package com.neueda.leap.sprint7;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CodeSmellScanner {

    private static final Pattern METHOD_START = Pattern.compile(
            "^\\s*(public|private|protected|static)[\\w<>\\[\\],\\s]*\\s+\\w+\\s*\\(([^)]*)\\)\\s*(throws\\s+[\\w,\\s]+)?\\s*\\{\\s*$");
    private static final Pattern STATIC_FIELD = Pattern.compile(
            "^\\s*static\\s+(?!final\\b)[\\w<>\\[\\],\\s]+\\s+\\w+\\s*[=;]");
    private static final Pattern DECISION_POINT = Pattern.compile(
            "\\b(if|for|while|catch|case)\\s*\\(|&&|\\|\\|");
    private static final Pattern DECIMAL_LITERAL = Pattern.compile("\\b\\d+\\.\\d+\\b");

    public static void main(String[] args) throws IOException {
        Path file = Path.of(args.length > 0 ? args[0]
                : "../../shared/starter-codebase/src/main/java/com/neueda/leap/sprint7/legacy/TradeReportGenerator.java");
        List<String> lines = Files.readAllLines(file);

        System.out.println("=== Code Smell Scan: " + file.getFileName() + " ===");
        System.out.println("Total lines: " + lines.size());
        System.out.println();

        scanMethods(lines);
        scanStaticFields(lines);
        scanDuplicatedLiterals(lines);
    }

    private static void scanMethods(List<String> lines) {
        System.out.println("-- Method length & complexity --");
        int depth = 0;
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            Matcher m = METHOD_START.matcher(line);
            if (m.matches() && depth == 1) {
                int startDepth = depth;
                int startLine = i;
                int paramCount = m.group(2) == null || m.group(2).isBlank() ? 0 : m.group(2).split(",").length;
                depth += countChar(line, '{') - countChar(line, '}');
                int j = i + 1;
                int decisionPoints = 0;
                while (j < lines.size() && depth > startDepth) {
                    String bodyLine = lines.get(j);
                    depth += countChar(bodyLine, '{') - countChar(bodyLine, '}');
                    decisionPoints += countMatches(DECISION_POINT, bodyLine);
                    j++;
                }
                int endLine = j - 1;
                int methodLength = endLine - startLine + 1;
                int complexity = decisionPoints + 1;
                System.out.printf("  %s%n", line.trim());
                System.out.printf("    length: %d lines | parameters: %d | approx. cyclomatic complexity: %d%n",
                        methodLength, paramCount, complexity);
                if (methodLength > 30) {
                    System.out.println("    -> LONG METHOD: over 30 lines is a strong signal it's doing more than one job");
                }
                if (complexity > 5) {
                    System.out.println("    -> HIGH COMPLEXITY: " + complexity + " distinct paths through this method");
                }
                i = endLine;
            } else {
                depth += countChar(line, '{') - countChar(line, '}');
            }
        }
        System.out.println();
    }

    private static void scanStaticFields(List<String> lines) {
        System.out.println("-- Mutable static state --");
        List<String> found = new ArrayList<>();
        for (String line : lines) {
            if (STATIC_FIELD.matcher(line).find()) {
                found.add(line.trim());
            }
        }
        System.out.println("  " + found.size() + " mutable static field(s) found:");
        for (String f : found) {
            System.out.println("    " + f);
        }
        System.out.println();
    }

    private static void scanDuplicatedLiterals(List<String> lines) {
        System.out.println("-- Duplicated literals --");
        Map<String, Integer> counts = new LinkedHashMap<>();
        for (String line : lines) {
            Matcher m = DECIMAL_LITERAL.matcher(line);
            while (m.find()) {
                counts.merge(m.group(), 1, Integer::sum);
            }
        }
        boolean anyDuplicates = false;
        for (Map.Entry<String, Integer> entry : counts.entrySet()) {
            if (entry.getValue() > 1) {
                anyDuplicates = true;
                System.out.println("  \"" + entry.getKey() + "\" appears " + entry.getValue()
                        + " times -> extract to a named constant");
            }
        }
        if (!anyDuplicates) {
            System.out.println("  none found");
        }
        System.out.println();
    }

    private static int countChar(String s, char c) {
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == c) count++;
        }
        return count;
    }

    private static int countMatches(Pattern p, String s) {
        Matcher m = p.matcher(s);
        int count = 0;
        while (m.find()) count++;
        return count;
    }
}
