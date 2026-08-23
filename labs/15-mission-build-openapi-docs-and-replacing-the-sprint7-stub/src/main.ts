import "reflect-metadata";
import { NestFactory } from "@nestjs/core";
import { ValidationPipe } from "@nestjs/common";
// TODO 3: import { DocumentBuilder, SwaggerModule } from "@nestjs/swagger" here.
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true }));

  // TODO 3: build a DocumentBuilder with a title, description, and version,
  // call SwaggerModule.createDocument(app, config), then
  // SwaggerModule.setup("api", app, document) - see Module 15's demo for
  // the exact shape.

  await app.listen(3000);
  console.log("Listening on http://localhost:3000");
}

bootstrap();
