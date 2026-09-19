package com.neueda.leap.sprint7;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

// KATA: the demo's scanner, with one check missing. scanDuplicatedLiterals()
// is called from main() but doesn't do anything yet - implement it so it
// finds decimal literals that appear MORE THAN ONCE in the file, which is a
// different (and arguably worse) smell than a magic number that only
// appears once: a duplicated literal can drift out of sync when only one
// copy gets updated.
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

    // TODO 1: count how many times each distinct decimal literal (e.g.
    //         "0.0005") appears across ALL lines of the file.
    // TODO 2: for every literal that appears MORE THAN ONCE, print it and
    //         its count, e.g.:
    //           "0.0005" appears 2 times -> extract to a named constant
    // TODO 3: if no literal appears more than once, print "  none found"
    //
    // Hint: DECIMAL_LITERAL.matcher(line) gives you each match on a line via
    // .find() / .group(); a Map<String, Integer> is enough to track counts.
    private static void scanDuplicatedLiterals(List<String> lines) {
        System.out.println("-- Duplicated literals --");
        // (implement here)
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
