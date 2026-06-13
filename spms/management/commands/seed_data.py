from django.core.management.base import BaseCommand
from spms.models import User, PointRule, Achievement
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = 'Seed the database with initial point rules and demo users'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding StudExa database...')

        # ── POINT RULES ──
        rules = [
            ('hackathon', 'national', 'winner', 50, 'Hackathon Winner — National'),
            ('hackathon', 'international', 'winner', 70, 'Hackathon Winner — International'),
            ('hackathon', 'national', 'runner_up', 35, 'Hackathon Runner Up — National'),
            ('hackathon', 'international', 'runner_up', 50, 'Hackathon Runner Up — International'),
            ('hackathon', 'any', 'participation', 10, 'Hackathon Participation'),
            ('research', 'any', 'published_indexed', 60, 'Research Paper — Indexed (Scopus/SCI)'),
            ('research', 'international', 'published_conference', 40, 'Research Paper — International Conference'),
            ('research', 'national', 'published_conference', 25, 'Research Paper — National Conference'),
            ('patent', 'any', 'granted', 100, 'Patent — Granted'),
            ('patent', 'any', 'filed', 50, 'Patent — Filed/Published'),
            ('certificate', 'any', 'premium', 30, 'Certificate — Premium (AWS/Google/Microsoft)'),
            ('certificate', 'any', 'standard', 15, 'Certificate — Standard (NPTEL/Coursera)'),
        ]

        created_rules = 0
        for cat, level, result, pts, desc in rules:
            obj, created = PointRule.objects.get_or_create(
                category=cat, level=level, result=result,
                defaults={'points': pts, 'description': desc}
            )
            if created:
                created_rules += 1
        self.stdout.write(f'  ✅ {created_rules} point rules created')

        # ── ADMIN USER ──
        if not User.objects.filter(username='admin@spms.com').exists():
            admin = User.objects.create_superuser(
                username='admin@spms.com',
                email='admin@spms.com',
                password='admin123',
                first_name='System',
                last_name='Admin',
                role='admin',
            )
            self.stdout.write('  ✅ Admin user: admin@spms.com / admin123')
        else:
            self.stdout.write('  ⚡ Admin user already exists')

        # ── FACULTY USER ──
        if not User.objects.filter(username='faculty@spms.com').exists():
            faculty = User.objects.create_user(
                username='faculty@spms.com',
                email='faculty@spms.com',
                password='faculty123',
                first_name='Dr. Priya',
                last_name='Nair',
                role='faculty',
                department='Computer Science',
            )
            self.stdout.write('  ✅ Faculty: faculty@spms.com / faculty123')

        # No demo student users — students will register themselves

        self.stdout.write(self.style.SUCCESS('\n🎉 StudExa database seeded successfully!\n'))
        self.stdout.write('Login credentials:')
        self.stdout.write('  Admin:   admin@spms.com   / admin123')
        self.stdout.write('  Faculty: faculty@spms.com / faculty123')
        self.stdout.write('  Students can register at /register/')
