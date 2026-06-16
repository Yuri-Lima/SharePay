import { NestFactory } from '@nestjs/core';
import helmet from 'helmet';
import { AppModule } from './app/app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // High-impact security headers
  app.use(helmet());

  // Global API prefix as required: /api/...
  app.setGlobalPrefix('api');

  // CORS permissive for dev (tighten in prod via env)
  app.enableCors({
    origin: true,
    credentials: true,
  });

  const port = (process.env as any).PORT || 3000;
  await app.listen(port);
  // eslint-disable-next-line no-console
  console.log(`SharePay API running on http://localhost:${port}/api`);
}
bootstrap();
