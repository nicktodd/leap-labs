package com.neueda.leap.sprint7;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

// A small, real static-analysis tool: not a toy print statement, but code
// that actually walks a .java file and measures the things "code quality"
// usually means in vague terms - method length, decision-point count,
// mutable static state, swallowed exceptions, and magic numbers. This is a
// simplified precursor to what Module 12's real SonarQube setup automates.
public class CodeSmellScanner {

    private static final Pattern METHOD_START = Pattern.compile(
            "^\\s*(public|private|protected|static)[\\w<>\\[\\],\\s]*\\s+\\w+\\s*\\(([^)]*)\\)\\s*(throws\\s+[\\w,\\s]+)?\\s*\\{\\s*$");
    private static final Pattern STATIC_FIELD = Pattern.compile(
            "^\\s*static\\s+(?!final\\b)[\\w<>\\[\\],\\s]+\\s+\\w+\\s*[=;]");
    private static final Pattern DECISION_POINT = Pattern.compile(
            "\\b(if|for|while|catch|case)\\s*\\(|&&|\\|\\|");
    private static final Pattern DECIMAL_LITERAL = Pattern.compile("\\b\\d+\\.\\d+\\b");
    private static final Pattern SHORT_VAR = Pattern.compile(
            "\\b(String|double|int|float|long|boolean)\\s+([a-zA-Z][a-zA-Z0-9]?)\\b\\s*[=;]");

    public static void main(String[] args) throws IOException {
        Path file = Path.of(args.length > 0 ? args[0]
                : "../../shared/starter-codebase/src/main/java/com/neueda/leap/sprint7/legacy/TradeReportGenerator.java");
        List<String> lines = Files.readAllLines(file);

        System.out.println("=== Code Smell Scan: " + file.getFileName() + " ===");
        System.out.println("Total lines: " + lines.size());
        System.out.println();

        scanMethods(lines);
        scanStaticFields(lines);
        scanEmptyCatchBlocks(lines);
        scanMagicNumbers(lines);
        scanShortVariableNames(lines);
    }

    private static void scanMethods(List<String> lines) {
        System.out.println("-- Method length & complexity --");
        int depth = 0;
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            Matcher m = METHOD_START.matcher(line);
            if (m.matches() && depth == 1) { // a method directly inside the class body
                int startDepth = depth;
                int startLine = i;
                int paramCount = countParams(m.group(2));
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
                String signature = line.trim();
                System.out.printf("  %s%n", signature);
                System.out.printf("    length: %d lines | parameters: %d | approx. cyclomatic complexity: %d%n",
                        methodLength, paramCount, complexity);
                if (methodLength > 30) {
                    System.out.println("    -> LONG METHOD: over 30 lines is a strong signal it's doing more than one job");
                }
                if (complexity > 5) {
                    System.out.println("    -> HIGH COMPLEXITY: " + complexity + " decision points means "
                            + complexity + " distinct paths through this method to reason about (and test)");
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
        if (!found.isEmpty()) {
            System.out.println("  -> Static mutable state is shared, global, and reset only by JVM restart -");
            System.out.println("     calling doIt() twice in the same run would accumulate, not reset.");
        }
        System.out.println();
    }

    private static void scanEmptyCatchBlocks(List<String> lines) {
        System.out.println("-- Swallowed exceptions --");
        int flagged = 0;
        for (int i = 0; i < lines.size(); i++) {
            if (lines.get(i).contains("catch") && lines.get(i).contains("(")) {
                int j = i + 1;
                boolean onlyCommentsOrBlank = true;
                while (j < lines.size() && !lines.get(j).trim().startsWith("}")) {
                    String body = lines.get(j).trim();
                    if (!body.isEmpty() && !body.startsWith("//")) {
                        onlyCommentsOrBlank = false;
                    }
                    j++;
                }
                if (onlyCommentsOrBlank) {
                    flagged++;
                    System.out.println("  line " + (i + 1) + ": " + lines.get(i).trim());
                    System.out.println("    -> catch block has no code - any exception here is silently discarded");
                }
            }
        }
        if (flagged == 0) {
            System.out.println("  none found");
        }
        System.out.println();
    }

    private static void scanMagicNumbers(List<String> lines) {
        System.out.println("-- Magic numbers --");
        Set<String> distinctValues = new LinkedHashSet<>();
        int total = 0;
        for (String line : lines) {
            Matcher m = DECIMAL_LITERAL.matcher(line);
            while (m.find()) {
                distinctValues.add(m.group());
                total++;
            }
        }
        System.out.println("  " + total + " unexplained decimal literal(s), " + distinctValues.size()
                + " distinct value(s): " + distinctValues);
        if (!distinctValues.isEmpty()) {
            System.out.println("  -> What do these numbers MEAN? Nothing in the code says - a named constant");
            System.out.println("     (EQUITY_FEE_RATE = 0.001) would answer that without needing a comment.");
        }
        System.out.println();
    }

    private static void scanShortVariableNames(List<String> lines) {
        System.out.println("-- Unclear naming (1-2 character identifiers) --");
        Set<String> names = new LinkedHashSet<>();
        for (String line : lines) {
            Matcher m = SHORT_VAR.matcher(line);
            while (m.find()) {
                names.add(m.group(2));
            }
        }
        System.out.println("  " + names.size() + " short local variable name(s): " + names);
        if (!names.isEmpty()) {
            System.out.println("  -> A name should say WHAT a value is. 'q' compiles identically to 'quantity' -");
            System.out.println("     only one of them tells the next reader anything.");
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

    private static int countParams(String paramList) {
        if (paramList == null || paramList.isBlank()) return 0;
        return paramList.split(",").length;
    }
}
