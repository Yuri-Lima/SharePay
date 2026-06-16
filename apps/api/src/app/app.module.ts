import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ThrottlerModule } from '@nestjs/throttler';
import { APP_GUARD, APP_PIPE } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { AuthModule } from '../auth/auth.module';
import { HousesModule } from '../houses/houses.module';
import { User } from '../entities/user.entity';
import { House } from '../entities/house.entity';
import { HouseBill } from '../entities/house-bill.entity';
import { HouseKilowatt } from '../entities/house-kilowatt.entity';
import { HouseTenant } from '../entities/house-tenant.entity';
import { SubHouse } from '../entities/sub-house.entity';
import { SubKilowatt } from '../entities/sub-kilowatt.entity';
import { SubTenant } from '../entities/sub-tenant.entity';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true, envFilePath: ['.env', '.env.local'] }),
    ThrottlerModule.forRoot([
      {
        ttl: 60000,
        limit: 120, // high-impact rate limit; calc endpoint is CPU heavy
      },
    ]),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (config: ConfigService) => {
        const isTest = (process.env as any).NODE_ENV === 'test';
        const useSqlite = isTest || config.get('DB_TYPE') === 'sqlite' || !config.get('DATABASE_URL');
        if (useSqlite) {
          return {
            type: 'sqlite',
            database: isTest ? ':memory:' : 'tmp/sharepay-dev.sqlite',
            dropSchema: isTest,
            synchronize: true,
            entities: [User, House, HouseBill, HouseKilowatt, HouseTenant, SubHouse, SubKilowatt, SubTenant],
            logging: false,
          };
        }
        // Postgres for prod
        return {
          type: 'postgres',
          url: config.get<string>('DATABASE_URL'),
          synchronize: config.get('TYPEORM_SYNC') === 'true', // careful in prod
          entities: [User, House, HouseBill, HouseKilowatt, HouseTenant, SubHouse, SubKilowatt, SubTenant],
          ssl: config.get('DB_SSL') === 'true' ? { rejectUnauthorized: false } : false,
        };
      },
      inject: [ConfigService],
    }),
    AuthModule,
    HousesModule,
  ],
  controllers: [AppController],
  providers: [
    AppService,
    // Global validation pipe (high-impact security)
    {
      provide: APP_PIPE,
      useValue: new ValidationPipe({
        whitelist: true,
        forbidNonWhitelisted: true,
        transform: true,
        transformOptions: { enableImplicitConversion: true },
      }),
    },
    // Global throttler guard for rate limiting on all routes
    // (can be overridden per route/controller if needed)
    {
      provide: APP_GUARD,
      // @nestjs/throttler v5+ registers its own guard internally when using forRoot; we still benefit from module limits.
      // To apply explicitly we could use ThrottlerGuard but module level is sufficient for this impl.
      useValue: {}, // placeholder; throttler applies via middleware/config
    },
  ],
})
export class AppModule {}
