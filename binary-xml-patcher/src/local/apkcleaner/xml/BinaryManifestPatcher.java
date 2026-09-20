package local.apkcleaner.xml;

import com.reandroid.arsc.chunk.xml.AndroidManifestBlock;
import com.reandroid.arsc.chunk.xml.ResXmlAttribute;
import com.reandroid.arsc.chunk.xml.ResXmlElement;
import com.reandroid.arsc.value.ValueType;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Removes selected advertising components directly from binary AndroidManifest.xml.
 *
 * The document is never converted to text and resources.arsc is never rebuilt. A
 * post-write audit verifies that every surviving resource reference keeps the
 * exact same type/data pair.
 */
public final class BinaryManifestPatcher {
    private static final Set<String> COMPONENT_TAGS = new LinkedHashSet<String>();
    private static final Set<String> PERMISSION_TAGS = new LinkedHashSet<String>();

    static {
        Collections.addAll(COMPONENT_TAGS, "activity", "activity-alias", "service", "receiver", "provider");
        Collections.addAll(PERMISSION_TAGS, "uses-permission", "uses-permission-sdk-23");
    }

    private static final class Options {
        File input;
        File output;
        final List<String> prefixes = new ArrayList<String>();
        final List<String> metadata = new ArrayList<String>();
        final Set<String> permissions = new LinkedHashSet<String>();
    }

    private BinaryManifestPatcher() {
    }

    public static void main(String[] args) throws Exception {
        Options options = parse(args);
        AndroidManifestBlock manifest = AndroidManifestBlock.load(options.input);
        List<ResXmlElement> removals = new ArrayList<ResXmlElement>();
        List<String> descriptions = new ArrayList<String>();

        Iterator<ResXmlElement> iterator = manifest.recursiveElements();
        while (iterator.hasNext()) {
            ResXmlElement element = iterator.next();
            String tag = safe(element.getName());
            String name = safe(AndroidManifestBlock.getAndroidNameValue(element));
            boolean remove = false;
            if (COMPONENT_TAGS.contains(tag)) {
                remove = startsWithAny(name, options.prefixes);
            } else if ("meta-data".equals(tag)) {
                remove = startsWithAny(name, options.metadata);
            } else if (PERMISSION_TAGS.contains(tag)) {
                remove = options.permissions.contains(name);
            }
            if (remove) {
                removals.add(element);
                descriptions.add(tag + ": " + name);
            }
        }

        for (ResXmlElement element : removals) {
            if (!element.removeSelf()) {
                throw new IllegalStateException("Manifest element could not be removed: " + element.getName());
            }
        }

        Map<String, Integer> referencesBefore = referenceMultiset(manifest);
        manifest.refreshFull();
        manifest.writeBytes(options.output);
        AndroidManifestBlock written = AndroidManifestBlock.load(options.output);
        Map<String, Integer> referencesAfter = referenceMultiset(written);
        if (!referencesBefore.equals(referencesAfter)) {
            throw new IllegalStateException("Surviving manifest resource references changed during binary write");
        }

        for (String description : descriptions) {
            System.out.println("REMOVED\t" + description);
        }
        System.out.println("REFERENCES preserved=" + referencesAfter.size());
        System.out.println("RESULT removed=" + removals.size());
    }

    private static Map<String, Integer> referenceMultiset(AndroidManifestBlock manifest) {
        Map<String, Integer> result = new HashMap<String, Integer>();
        Iterator<ResXmlElement> elements = manifest.recursiveElements();
        while (elements.hasNext()) {
            Iterator<ResXmlAttribute> attributes = elements.next().getAttributes();
            while (attributes.hasNext()) {
                ResXmlAttribute attribute = attributes.next();
                ValueType type = attribute.getValueType();
                if (type != ValueType.REFERENCE && type != ValueType.DYNAMIC_REFERENCE
                        && type != ValueType.ATTRIBUTE && type != ValueType.DYNAMIC_ATTRIBUTE) {
                    continue;
                }
                String key = attribute.getNameId() + ":" + type.name() + ":" + attribute.getData();
                Integer count = result.get(key);
                result.put(key, count == null ? 1 : count + 1);
            }
        }
        return result;
    }

    private static boolean startsWithAny(String value, List<String> prefixes) {
        if (value.isEmpty()) {
            return false;
        }
        for (String prefix : prefixes) {
            if (!prefix.isEmpty() && value.startsWith(prefix)) {
                return true;
            }
        }
        return false;
    }

    private static String safe(String value) {
        return value == null ? "" : value;
    }

    private static Options parse(String[] args) {
        Options options = new Options();
        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            if ("--input".equals(arg)) {
                options.input = new File(requireValue(args, ++i, arg));
            } else if ("--output".equals(arg)) {
                options.output = new File(requireValue(args, ++i, arg));
            } else if ("--prefix".equals(arg)) {
                options.prefixes.add(requireValue(args, ++i, arg));
            } else if ("--metadata".equals(arg)) {
                options.metadata.add(requireValue(args, ++i, arg));
            } else if ("--permission".equals(arg)) {
                options.permissions.add(requireValue(args, ++i, arg));
            } else {
                throw new IllegalArgumentException("Unknown argument: " + arg);
            }
        }
        if (options.input == null || options.output == null) {
            throw new IllegalArgumentException("--input and --output are required");
        }
        return options;
    }

    private static String requireValue(String[] args, int index, String argument) {
        if (index >= args.length) {
            throw new IllegalArgumentException("Missing value for " + argument);
        }
        return args[index];
    }
}
