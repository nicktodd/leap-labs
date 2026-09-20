import "reflect-metadata";
import { NestFactory } from "@nestjs/core";
import { ValidationPipe } from "@nestjs/common";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // A GLOBAL ValidationPipe - applied to every route in the app, not just
  // one. whitelist strips any property NOT declared on the DTO;
  // forbidNonWhitelisted rejects the request outright if one is present,
  // instead of silently dropping it.
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
    }),
  );

  await app.listen(3000);
  console.log("Listening on http://localhost:3000");
}

bootstrap();
