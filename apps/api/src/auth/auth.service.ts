import { Injectable, UnauthorizedException, ConflictException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import * as bcrypt from 'bcrypt';
import { JwtService } from '@nestjs/jwt';
import { User } from '../entities/user.entity';
import { RegisterDto } from './dto/register.dto';

@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepo: Repository<User>,
    private readonly jwtService: JwtService,
  ) {}

  async register(dto: RegisterDto): Promise<{ access_token: string; user: { id: number; username: string } }> {
    const existing = await this.usersRepo.findOne({ where: { username: dto.username } });
    if (existing) {
      throw new ConflictException('Username already exists');
    }
    const salt = await bcrypt.genSalt(10);
    const hash = await bcrypt.hash(dto.password, salt);
    const user = this.usersRepo.create({ username: dto.username, password: hash });
    const saved = await this.usersRepo.save(user);
    const payload = { sub: saved.id, username: saved.username };
    const access_token = await this.jwtService.signAsync(payload);
    return { access_token, user: { id: saved.id, username: saved.username } };
  }

  async validateUser(username: string, pass: string): Promise<any> {
    const user = await this.usersRepo.findOne({ where: { username } });
    if (!user) return null;
    const isMatch = await bcrypt.compare(pass, user.password);
    if (!isMatch) return null;
    const { password, ...result } = user;
    return result;
  }

  async login(user: any) {
    const payload = { sub: user.id, username: user.username };
    return {
      access_token: await this.jwtService.signAsync(payload),
      user: { id: user.id, username: user.username },
    };
  }
}
