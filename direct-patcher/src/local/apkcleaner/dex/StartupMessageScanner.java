package local.apkcleaner.dex;

import com.android.tools.smali.dexlib2.Opcode;
import com.android.tools.smali.dexlib2.Opcodes;
import com.android.tools.smali.dexlib2.dexbacked.DexBackedDexFile;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
import java.nio.file.*;
import java.util.*;

/** Read-only, bounded, cross-DEX lifecycle call tracing. Never claims provenance. */
final class StartupMessageScanner {
    private final Map<String, ClassDef> classes = new LinkedHashMap<>();
    // Index only classes visited by the trace. Large multidex apps can contain
    // hundreds of thousands of unrelated methods; retaining every signature
    // wastes mobile heap and used to reject them before scanning any roots.
    private final Map<String, Map<String, Method>> methodCache =
        new LinkedHashMap<String, Map<String, Method>>(64, .75f, true) {
            @Override protected boolean removeEldestEntry(Map.Entry<String, Map<String, Method>> entry) {
                return size() > 256;
            }
        };
    private final Map<String, String> dexNames = new HashMap<>();
    private static final Set<String> ACTIVITY_BASES = new HashSet<>(Arrays.asList(
        "Landroid/app/Activity;", "Landroidx/activity/ComponentActivity;",
        "Landroidx/core/app/ComponentActivity;", "Landroidx/fragment/app/FragmentActivity;",
        "Landroidx/appcompat/app/AppCompatActivity;", "Landroid/support/v4/app/FragmentActivity;",
        "Landroid/support/v7/app/AppCompatActivity;"));
    private static final Set<String> STARTUP_BASES = new HashSet<>(ACTIVITY_BASES);
    static { STARTUP_BASES.addAll(Arrays.asList("Landroid/app/Application;", "Landroid/app/Fragment;",
        "Landroidx/fragment/app/Fragment;", "Landroid/support/v4/app/Fragment;")); }
    private static final class Evidence {
        String sink = "", kind = "";
        final List<String> trace = new ArrayList<>();
        boolean mixed, limited, deferred;
        int instructions;
        final Set<String> visited = new HashSet<>();
    }

    static String key(MethodReference method) {
        return method.getDefiningClass() + "->" + method.getName() + method.getParameterTypes() + method.getReturnType();
    }

    static boolean lifecycle(Method method) {
        if ((method.getAccessFlags() & 8) != 0) return false;
        String name = method.getName();
        String params = method.getParameterTypes().toString();
        if ("onCreateView".equals(name) && "Landroid/view/View;".equals(method.getReturnType()))
            return "[Landroid/view/LayoutInflater;, Landroid/view/ViewGroup;, Landroid/os/Bundle;]".equals(params);
        if (!"V".equals(method.getReturnType())) return false;
        return (Arrays.asList("onResume", "onStart", "onPostResume", "onRestart",
                "onAttachedToWindow", "onResumeFragments").contains(name) && "[]".equals(params))
            || ("onCreate".equals(name) && ("[Landroid/os/Bundle;]".equals(params)
                || "[]".equals(params) || "[Landroid/os/Bundle;, Landroid/os/PersistableBundle;]".equals(params)))
            || (Arrays.asList("onPostCreate", "onActivityCreated", "onViewStateRestored").contains(name)
                && "[Landroid/os/Bundle;]".equals(params))
            || ("onViewCreated".equals(name) && "[Landroid/view/View;, Landroid/os/Bundle;]".equals(params))
            || ("onNewIntent".equals(name) && "[Landroid/content/Intent;]".equals(params))
            || ("onWindowFocusChanged".equals(name) && "[Z]".equals(params));
    }

    static boolean rootCall(Instruction instruction, MethodReference target) {
        String opcode = instruction.getOpcode().name();
        return (opcode.startsWith("INVOKE_STATIC") || opcode.startsWith("INVOKE_DIRECT")
            || opcode.startsWith("INVOKE_VIRTUAL") || opcode.startsWith("INVOKE_INTERFACE"))
            && !target.getName().startsWith("<") && !platform(target.getDefiningClass());
    }

    static boolean unusedResult(List<Instruction> instructions, int index) {
        return index + 1 >= instructions.size() || !instructions.get(index + 1).getOpcode().name().startsWith("MOVE_RESULT");
    }

    private boolean startupMethod(ClassDef cls, Method method) {
        if (!lifecycle(method)) return false;
        if (derives(cls.getType(), Collections.singleton("Landroid/app/Application;")))
            return method.getName().equals("onCreate") && method.getParameterTypes().isEmpty();
        if (method.getName().equals("onCreate") && method.getParameterTypes().isEmpty()) return false;
        if (derives(cls.getType(), ACTIVITY_BASES))
            return !Arrays.asList("onActivityCreated", "onViewCreated", "onViewStateRestored", "onCreateView").contains(method.getName());
        return !Arrays.asList("onPostCreate", "onPostResume", "onRestart", "onNewIntent",
            "onAttachedToWindow", "onWindowFocusChanged", "onResumeFragments").contains(method.getName());
    }

    static String execute(String[] args) throws Exception {
        StartupMessageScanner scan = new StartupMessageScanner();
        long total = 0;
        for (int i = 1; i < args.length; i += 3) {
            if (i + 2 >= args.length || !"--dex".equals(args[i])) throw new IllegalArgumentException("Geçersiz DEX tarama isteği.");
            Path path = Paths.get(args[i + 2]);
            total += Files.size(path);
            if (total > 256L * 1024 * 1024) throw new IllegalArgumentException("Başlangıç taraması için toplam DEX boyutu 256 MB sınırını aşıyor.");
            DexBackedDexFile dex = new DexBackedDexFile(Opcodes.getDefault(), Files.readAllBytes(path));
            for (ClassDef cls : dex.getClasses()) {
                if (scan.classes.put(cls.getType(), cls) != null) throw new IllegalArgumentException("Yinelenen DEX sınıfı; güvenli çağrı çözümlemesi yapılamadı.");
                scan.dexNames.put(cls.getType(), args[i + 1]);
                if (scan.classes.size() > 150000) throw new IllegalArgumentException("Başlangıç taraması sınıf sınırını aşıyor.");
            }
        }
        return scan.scan();
    }

    private static boolean platform(String type) {
        return type.startsWith("Landroid/") || type.startsWith("Landroidx/") || type.startsWith("Ljava/")
            || type.startsWith("Ljavax/") || type.startsWith("Lkotlin/");
    }

    private boolean derives(String type, Set<String> bases) {
        Set<String> seen = new HashSet<>();
        while (type != null && seen.add(type)) {
            if (bases.contains(type)) return true;
            ClassDef cls = classes.get(type);
            if (cls == null) break;
            for (String iface : cls.getInterfaces()) if (bases.contains(iface)) return true;
            type = cls.getSuperclass();
        }
        return false;
    }

    private String scan() throws Exception {
        StringBuilder result = new StringBuilder();
        int count = 0;
        for (ClassDef cls : classes.values()) {
            if (!derives(cls.getType(), STARTUP_BASES)) continue;
            for (Method owner : cls.getMethods()) {
                if (!startupMethod(cls, owner) || owner.getImplementation() == null) continue;
                MethodImplementation body = owner.getImplementation();
                int thisRegister = body.getRegisterCount() - owner.getParameterTypes().size() - 1;
                Set<Integer> aliases = new HashSet<>(); aliases.add(thisRegister);
                List<Instruction> instructions = new ArrayList<>();
                body.getInstructions().forEach(instructions::add);
                // Aliases which are never repurposed remain valid beyond an if/goto.
                Set<Integer> stableAliases = stableAliases(instructions, thisRegister);
                Map<Integer, String> objects = initialTypes(owner);
                Map<Integer, String> threads = new HashMap<>();
                // Absence of a super call is not evidence of an early injection.
                boolean beforeSuper = false;
                for (Instruction instruction : instructions) {
                    MethodReference parent = reference(instruction);
                    if (parent != null && instruction.getOpcode().name().startsWith("INVOKE_SUPER")
                        && owner.getName().equals(parent.getName())
                        && owner.getParameterTypes().toString().equals(parent.getParameterTypes().toString())) {
                        beforeSuper = true;
                        break;
                    }
                }
                for (int index = 0; index < instructions.size(); index++) {
                    Instruction ins = instructions.get(index);
                    MethodReference target = reference(ins);
                    if (target != null && (ins.getOpcode() == Opcode.INVOKE_SUPER || ins.getOpcode() == Opcode.INVOKE_SUPER_RANGE)
                        && owner.getName().equals(target.getName())) beforeSuper = false;
                    Method resolved = target == null ? null : resolveCall(ins, target, objects);
                    boolean hasOwner = false;
                    for (int reg : registers(ins)) if (aliases.contains(reg)) hasOwner = true;
                    boolean staticCall = ins.getOpcode().name().startsWith("INVOKE_STATIC");
                    boolean independent = target != null && staticCall && target.getParameterTypes().isEmpty();
                    boolean knownReceiver = !staticCall && objects.containsKey(firstRegister(ins));
                    if (target != null && rootCall(ins, target) && unusedResult(instructions, index)
                        && (hasOwner || independent || knownReceiver) && resolved != null && resolved.getImplementation() != null
                        && !lifecycle(resolved) && sinkKind(target) == null) {
                        Evidence found = new Evidence();
                        trace(resolved, found, new ArrayList<>(), 0, bindArguments(resolved, ins, objects));
                        if (!found.sink.isEmpty()) {
                            if (++count > 250) throw new IllegalArgumentException("Çok fazla başlangıç adayı; tarama daraltılamadı.");
                            String id = DirectDexPatcher.startupIdentity(cls, owner, target, ins);
                            String reason = beforeSuper ? "before_super" : "lifecycle";
                            result.append("STARTUP\t").append(dexNames.get(cls.getType())).append('\t').append(id)
                                .append('\t').append(found.kind).append('\t').append(cls.getType()).append('\t').append(owner.getName())
                                .append('\t').append(target.getDefiningClass()).append('\t').append(target.getName())
                                .append('\t').append(reason).append('\t').append(found.limited ? "partial" : found.mixed ? "review" : "candidate")
                                .append('\t').append(found.deferred ? "deferred" : "direct")
                                .append('\t').append(String.join(" > ", found.trace)).append('\n');
                        }
                    }
                    trackAlias(ins, aliases, stableAliases);
                    trackObjects(ins, objects, threads, Collections.emptyMap());
                    for (int alias : aliases) objects.put(alias, cls.getType());
                }
            }
        }
        return result.toString();
    }

    // Narrow dataflow: only the activity instance (or a move-object alias) qualifies.
    private static Set<Integer> stableAliases(List<Instruction> instructions, int thisRegister) {
        Map<Integer, Set<Integer>> moves = new HashMap<>();
        Set<Integer> overwritten = new HashSet<>();
        for (Instruction ins : instructions) {
            if (ins.getOpcode() == Opcode.CHECK_CAST) continue;
            if (!ins.getOpcode().setsRegister() || !(ins instanceof OneRegisterInstruction)) continue;
            int dest = ((OneRegisterInstruction) ins).getRegisterA();
            if (ins.getOpcode().name().startsWith("MOVE_OBJECT") && ins instanceof TwoRegisterInstruction)
                moves.computeIfAbsent(dest, k -> new HashSet<>()).add(((TwoRegisterInstruction) ins).getRegisterB());
            else overwritten.add(dest);
        }
        Set<Integer> stable = new HashSet<>();
        if (!overwritten.contains(thisRegister) && !moves.containsKey(thisRegister)) stable.add(thisRegister);
        boolean changed;
        do { changed = false;
            for (Map.Entry<Integer, Set<Integer>> move : moves.entrySet())
                if (!overwritten.contains(move.getKey()) && stable.containsAll(move.getValue())) changed |= stable.add(move.getKey());
        } while (changed);
        return stable;
    }

    private static void trackAlias(Instruction ins, Set<Integer> aliases, Set<Integer> stable) {
        if (ins.getOpcode() == Opcode.CHECK_CAST) return;
        if ((ins.getOpcode() == Opcode.MOVE_OBJECT || ins.getOpcode() == Opcode.MOVE_OBJECT_FROM16
            || ins.getOpcode() == Opcode.MOVE_OBJECT_16) && ins instanceof TwoRegisterInstruction) {
            TwoRegisterInstruction move = (TwoRegisterInstruction) ins;
            if (aliases.contains(move.getRegisterB())) aliases.add(move.getRegisterA()); else aliases.remove(move.getRegisterA());
        } else if (ins.getOpcode().setsRegister() && ins instanceof OneRegisterInstruction) {
            aliases.remove(((OneRegisterInstruction) ins).getRegisterA());
        }
        // Do not guess register provenance across branches or exception paths.
        if (ins instanceof OffsetInstruction || ins.getOpcode() == Opcode.MOVE_EXCEPTION) aliases.retainAll(stable);
    }

    private Map<Integer, String> initialTypes(Method method) {
        Map<Integer, String> types = new HashMap<>();
        int count = (method.getAccessFlags() & 8) == 0 ? 1 : 0;
        for (CharSequence type : method.getParameterTypes()) count += wide(type.toString()) ? 2 : 1;
        int reg = method.getImplementation().getRegisterCount() - count;
        if ((method.getAccessFlags() & 8) == 0) types.put(reg++, method.getDefiningClass());
        for (CharSequence type : method.getParameterTypes()) {
            if (type.toString().startsWith("L")) types.put(reg, type.toString());
            reg += wide(type.toString()) ? 2 : 1;
        }
        return types;
    }

    private static boolean wide(String type) { return type.equals("J") || type.equals("D"); }

    private Map<Integer, String> bindArguments(Method method, Instruction ins, Map<Integer, String> objects) {
        Map<Integer, String> types = initialTypes(method);
        int[] regs = registers(ins);
        int dest = method.getImplementation().getRegisterCount() - regs.length;
        for (int i = 0; i < regs.length; i++) if (objects.get(regs[i]) != null) types.put(dest + i, objects.get(regs[i]));
        return types;
    }

    private Method resolveCall(Instruction ins, MethodReference ref, Map<Integer, String> objects) {
        String opcode = ins.getOpcode().name();
        if (opcode.startsWith("INVOKE_VIRTUAL") || opcode.startsWith("INVOKE_INTERFACE")) {
            String actual = objects.get(firstRegister(ins));
            if (actual != null && derives(actual, Collections.singleton(ref.getDefiningClass()))) {
                Method concrete = declaredMethod(actual, ref);
                if (concrete != null && concrete.getImplementation() != null) return concrete;
            }
        }
        return resolve(ref);
    }

    private Method declaredMethod(String type, MethodReference ref) {
        ClassDef cls = classes.get(type);
        if (cls == null) return null;
        Map<String, Method> declared = methodCache.get(type);
        if (declared == null) {
            declared = new HashMap<>();
            for (Method method : cls.getMethods()) declared.put(key(method), method);
            methodCache.put(type, declared);
        }
        return declared.get(type + "->" + ref.getName() + ref.getParameterTypes() + ref.getReturnType());
    }

    private Method resolve(MethodReference ref) {
        Method method = declaredMethod(ref.getDefiningClass(), ref);
        if (method != null) return method;
        String type = ref.getDefiningClass();
        Set<String> seen = new HashSet<>();
        while (seen.add(type) && classes.containsKey(type)) {
            type = classes.get(type).getSuperclass();
            if (type == null) break;
            method = declaredMethod(type, ref);
            if (method != null) return method;
        }
        return null;
    }

    private void trace(Method method, Evidence found, List<String> chain, int depth, Map<Integer, String> arguments) {
        if (method == null || method.getImplementation() == null) { found.mixed = true; return; }
        String visit = key(method) + new TreeMap<>(arguments);
        if (found.visited.contains(visit)) return;
        if (depth > 24 || found.visited.size() >= 1024) { found.limited = true; return; }
        found.visited.add(visit);
        List<String> path = new ArrayList<>(chain); path.add(key(method));
        Map<Integer, String> objects = new HashMap<>(arguments);
        Map<Integer, String> stableObjects = stableTypes(method, arguments);
        Map<Integer, String> threadTasks = new HashMap<>();
        for (Instruction ins : method.getImplementation().getInstructions()) {
            if (++found.instructions > 80000 || Thread.currentThread().isInterrupted()) { found.limited = true; return; }
            MethodReference ref = reference(ins);
            if (ref != null) {
                String sink = sinkKind(ref);
                if (sink != null && found.sink.isEmpty()) {
                    found.sink = key(ref); found.kind = sink;
                    found.trace.addAll(path); found.trace.add(key(ref));
                }
                String name = ref.getName(), type = ref.getDefiningClass();
                int[] regs = registers(ins);
                if ("Ljava/lang/Thread;".equals(type) && "<init>".equals(name) && regs.length > 1
                    && ref.getParameterTypes().toString().equals("[Ljava/lang/Runnable;]")) {
                    threadTasks.put(regs[0], objects.get(regs[1]));
                }
                if (name.equals("post") || name.equals("postDelayed") || name.equals("runOnUiThread") || name.equals("execute")) {
                    boolean scheduler = derives(type, new HashSet<>(Arrays.asList("Landroid/os/Handler;", "Landroid/view/View;", "Landroid/app/Activity;")))
                        || type.startsWith("Ljava/util/concurrent/");
                    if (scheduler && ref.getParameterTypes().size() > 0 && "Ljava/lang/Runnable;".equals(ref.getParameterTypes().get(0).toString()) && regs.length > 1) {
                        followCallback(objects.get(regs[1]), "run", found, path, depth);
                    }
                }
                if (name.equals("start") && "Ljava/lang/Thread;".equals(type) && regs.length > 0) {
                    followCallback(threadTasks.get(regs[0]), "run", found, path, depth);
                }
                if ((name.equals("execute") || name.equals("executeOnExecutor")) && regs.length > 0) {
                    String task = objects.get(regs[0]);
                    if (task != null && derives(task, Collections.singleton("Landroid/os/AsyncTask;"))) {
                        followCallback(task, "doInBackground", found, path, depth);
                        followCallback(task, "onPostExecute", found, path, depth);
                        followCallback(task, "onPreExecute", found, path, depth);
                    }
                }
                if (sink == null && !platform(type)) {
                    Method next = resolveCall(ins, ref, objects);
                    if (next != null && next.getImplementation() != null) trace(next, found, path, depth + 1, bindArguments(next, ins, objects));
                    else found.mixed = true; // Native, unresolved or opaque helper.
                }
                if (sensitive(ref)) found.mixed = true;
            }
            if (ins.getOpcode().name().startsWith("SPUT") || ins.getOpcode().name().startsWith("IPUT")) found.mixed = true;
            trackObjects(ins, objects, threadTasks, stableObjects);
        }
    }

    private void followCallback(String type, String name, Evidence found, List<String> path, int depth) {
        if (type == null || !classes.containsKey(type)) return;
        found.deferred = true;
        for (Method callback : classes.get(type).getMethods()) {
            if (name.equals(callback.getName()) && (name.equals("run") ? callback.getParameterTypes().isEmpty() : true))
                if (callback.getImplementation() != null) trace(callback, found, path, depth + 1, initialTypes(callback));
        }
    }

    // Retain proven object types through obfuscator if/goto wrappers, including
    // local move-object copies of callback parameters. Never infer from names.
    private Map<Integer, String> stableTypes(Method method, Map<Integer, String> arguments) {
        Map<Integer, List<Instruction>> writes = new HashMap<>();
        for (Instruction ins : method.getImplementation().getInstructions()) {
            if (ins.getOpcode() == Opcode.CHECK_CAST || !ins.getOpcode().setsRegister() || !(ins instanceof OneRegisterInstruction)) continue;
            writes.computeIfAbsent(((OneRegisterInstruction) ins).getRegisterA(), k -> new ArrayList<>()).add(ins);
        }
        Map<Integer, String> stable = new HashMap<>(arguments);
        writes.keySet().forEach(stable::remove);
        boolean changed;
        do { changed = false;
            for (Map.Entry<Integer, List<Instruction>> entry : writes.entrySet()) {
                if (stable.containsKey(entry.getKey())) continue;
                String common = null; boolean valid = true;
                for (Instruction ins : entry.getValue()) {
                    String type = null;
                    if (ins.getOpcode().name().startsWith("MOVE_OBJECT") && ins instanceof TwoRegisterInstruction)
                        type = stable.get(((TwoRegisterInstruction) ins).getRegisterB());
                    else if (ins.getOpcode() == Opcode.NEW_INSTANCE)
                        type = ((TypeReference) ((ReferenceInstruction) ins).getReference()).getType();
                    if (type == null || (common != null && !common.equals(type))) { valid = false; break; }
                    common = type;
                }
                if (valid && common != null) { stable.put(entry.getKey(), common); changed = true; }
            }
        } while (changed);
        return stable;
    }

    private void trackObjects(Instruction ins, Map<Integer, String> objects, Map<Integer, String> threads, Map<Integer, String> stable) {
        if (ins.getOpcode() == Opcode.CHECK_CAST && ins instanceof ReferenceInstruction) {
            int reg = ((OneRegisterInstruction) ins).getRegisterA();
            String cast = ((TypeReference) ((ReferenceInstruction) ins).getReference()).getType();
            String actual = objects.get(reg);
            if (actual == null || !derives(actual, Collections.singleton(cast))) objects.put(reg, cast);
        } else if ((ins.getOpcode() == Opcode.IGET_OBJECT || ins.getOpcode() == Opcode.SGET_OBJECT) && ins instanceof ReferenceInstruction) {
            objects.put(((OneRegisterInstruction) ins).getRegisterA(), ((FieldReference) ((ReferenceInstruction) ins).getReference()).getType());
        } else if (ins.getOpcode() == Opcode.NEW_INSTANCE && ins instanceof ReferenceInstruction) {
            int reg = ((OneRegisterInstruction) ins).getRegisterA();
            objects.put(reg, ((TypeReference) ((ReferenceInstruction) ins).getReference()).getType());
            threads.remove(reg);
        } else if ((ins.getOpcode() == Opcode.MOVE_OBJECT || ins.getOpcode() == Opcode.MOVE_OBJECT_FROM16 || ins.getOpcode() == Opcode.MOVE_OBJECT_16) && ins instanceof TwoRegisterInstruction) {
            TwoRegisterInstruction move = (TwoRegisterInstruction) ins;
            objects.put(move.getRegisterA(), objects.get(move.getRegisterB()));
            threads.put(move.getRegisterA(), threads.get(move.getRegisterB()));
        } else if (ins.getOpcode().setsRegister() && ins instanceof OneRegisterInstruction) {
            objects.remove(((OneRegisterInstruction) ins).getRegisterA());
            threads.remove(((OneRegisterInstruction) ins).getRegisterA());
        }
        if (ins instanceof OffsetInstruction || ins.getOpcode() == Opcode.MOVE_EXCEPTION) {
            objects.keySet().retainAll(stable.keySet()); threads.clear();
        }
    }

    private String sinkKind(MethodReference ref) {
        String name = ref.getName(), type = ref.getDefiningClass();
        Set<String> dialogBases = new HashSet<>(Arrays.asList(
            "Landroid/app/Dialog;", "Landroid/app/AlertDialog;", "Landroidx/activity/ComponentDialog;",
            "Landroidx/appcompat/app/AppCompatDialog;", "Landroidx/appcompat/app/AlertDialog;",
            "Landroid/support/v7/app/AppCompatDialog;", "Landroid/support/v7/app/AlertDialog;",
            "Lcom/google/android/material/bottomsheet/BottomSheetDialog;",
            "Lcom/afollestad/materialdialogs/MaterialDialog;"));
        // Real framework types/signatures, not a method merely named show/update.
        if ("show".equals(name) && ref.getParameterTypes().isEmpty() && "V".equals(ref.getReturnType())) {
            if (derives(type, Collections.singleton("Landroid/widget/Toast;"))) return "Toast";
            if (derives(type, dialogBases)) return "Diyalog";
            if (derives(type, new HashSet<>(Arrays.asList("Lcom/google/android/material/snackbar/Snackbar;", "Lcom/google/android/material/snackbar/BaseTransientBottomBar;", "Landroid/support/design/widget/Snackbar;")))) return "Snackbar";
        }
        if ("show".equals(name) && ref.getParameterTypes().isEmpty()
            && ref.getReturnType().endsWith("AlertDialog;") && derives(type, new HashSet<>(Arrays.asList(
                "Landroid/app/AlertDialog$Builder;", "Landroidx/appcompat/app/AlertDialog$Builder;",
                "Landroid/support/v7/app/AlertDialog$Builder;", "Lcom/google/android/material/dialog/MaterialAlertDialogBuilder;")))) return "Diyalog";
        if ((name.equals("show") || name.equals("showNow")) && ref.getParameterTypes().size() == 2
            && derives(type, new HashSet<>(Arrays.asList("Landroid/app/DialogFragment;", "Landroidx/fragment/app/DialogFragment;", "Landroid/support/v4/app/DialogFragment;")))
            && (ref.getParameterTypes().get(0).toString().endsWith("FragmentManager;") || ref.getParameterTypes().get(0).toString().endsWith("FragmentTransaction;"))) return "Diyalog";
        if ("showDialog".equals(name) && derives(type, ACTIVITY_BASES) && ref.getParameterTypes().toString().equals("[I]")) return "Diyalog";
        if (derives(type, Collections.singleton("Landroid/widget/PopupWindow;"))
            && (name.equals("showAtLocation") || name.equals("showAsDropDown")) && "V".equals(ref.getReturnType())) return "Diyalog";
        if ((type.equals("Landroidx/compose/ui/window/AndroidDialog_androidKt;") && name.equals("Dialog"))
            || ((type.startsWith("Landroidx/compose/material/") || type.startsWith("Landroidx/compose/material3/"))
                && (name.equals("AlertDialog") || name.equals("BasicAlertDialog")))) return "Diyalog";
        return null;
    }

    private static boolean sensitive(MethodReference ref) {
        String key = key(ref).toLowerCase(Locale.ROOT), name = ref.getName();
        return key.contains("integrity") || key.contains("licens") || key.contains("billing") || key.contains("permission")
            || key.contains("java/net/") || key.contains("okhttp") || key.contains("retrofit") || key.contains("java/lang/reflect")
            || key.contains("sharedpreferences$editor") || key.contains("sqlite") || key.contains("java/io/fileoutput")
            || Arrays.asList("setContentView", "startActivity", "finish", "loadLibrary", "exit", "setDefaultUncaughtExceptionHandler").contains(name);
    }

    private static MethodReference reference(Instruction ins) {
        if (!ins.getOpcode().name().startsWith("INVOKE_") || !(ins instanceof ReferenceInstruction)) return null;
        Object ref = ((ReferenceInstruction) ins).getReference();
        return ref instanceof MethodReference ? (MethodReference) ref : null;
    }
    private static int firstRegister(Instruction ins) { int[] regs = registers(ins); return regs.length == 0 ? -1 : regs[0]; }
    private static int[] registers(Instruction ins) {
        if (ins instanceof RegisterRangeInstruction) {
            RegisterRangeInstruction range = (RegisterRangeInstruction) ins;
            int[] result = new int[range.getRegisterCount()];
            for (int i = 0; i < result.length; i++) result[i] = range.getStartRegister() + i;
            return result;
        }
        if (ins instanceof FiveRegisterInstruction) {
            FiveRegisterInstruction five = (FiveRegisterInstruction) ins;
            return Arrays.copyOf(new int[]{five.getRegisterC(), five.getRegisterD(), five.getRegisterE(), five.getRegisterF(), five.getRegisterG()}, five.getRegisterCount());
        }
        return new int[0];
    }
}
