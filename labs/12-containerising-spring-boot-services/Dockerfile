# Stage 1: build
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app

# Cache dependencies as a separate layer
COPY pom.xml .
RUN mvn -B dependency:go-offline

# Build the application
COPY src/ src/
RUN mvn -B clean package -DskipTests

# Stage 2: runtime (no JDK, no Maven - just enough to run a jar)
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
