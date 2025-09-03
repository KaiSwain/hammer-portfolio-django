from django.core.management.base import BaseCommand
from hammer_backendapi.models import (
    DiscAssessment, SixteenTypeAssessment, EnneagramResult, 
    GenderIdentity, OshaType, FundingSource, State, Region
)

class Command(BaseCommand):
    help = 'Populate database with personality assessment and reference data'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Populating database with assessment data...")
        self.stdout.write("=" * 60)
        
        self.populate_disc_assessments()
        self.populate_sixteen_types()
        self.populate_enneagram_results()
        self.populate_gender_identities()
        self.populate_osha_types()
        self.populate_funding_sources()
        self.populate_states()
        self.populate_regions()
        
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ Successfully populated all assessment data!"))

    def populate_disc_assessments(self):
        """Populate DISC Assessment types"""
        disc_types = [
            "D - Dominance",
            "I - Influence", 
            "S - Steadiness",
            "C - Conscientiousness",
            "DI - Dominance/Influence",
            "DC - Dominance/Conscientiousness", 
            "ID - Influence/Dominance",
            "IS - Influence/Steadiness",
            "SI - Steadiness/Influence",
            "SC - Steadiness/Conscientiousness",
            "CD - Conscientiousness/Dominance",
            "CS - Conscientiousness/Steadiness"
        ]
        
        created_count = 0
        for disc_type in disc_types:
            _, created = DiscAssessment.objects.get_or_create(
                type_name=disc_type
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created DISC type: {disc_type}")
        
        self.stdout.write(f"DISC Assessments: {created_count} new, {DiscAssessment.objects.count()} total")

    def populate_sixteen_types(self):
        """Populate 16 Personality Types (Myers-Briggs)"""
        sixteen_types = [
            "INTJ - The Architect",
            "INTP - The Thinker", 
            "ENTJ - The Commander",
            "ENTP - The Debater",
            "INFJ - The Advocate",
            "INFP - The Mediator",
            "ENFJ - The Protagonist", 
            "ENFP - The Campaigner",
            "ISTJ - The Logistician",
            "ISFJ - The Protector",
            "ESTJ - The Executive",
            "ESFJ - The Consul",
            "ISTP - The Virtuoso",
            "ISFP - The Adventurer",
            "ESTP - The Entrepreneur", 
            "ESFP - The Entertainer"
        ]
        
        created_count = 0
        for type_name in sixteen_types:
            _, created = SixteenTypeAssessment.objects.get_or_create(
                type_name=type_name
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created 16 Type: {type_name}")
        
        self.stdout.write(f"16 Personality Types: {created_count} new, {SixteenTypeAssessment.objects.count()} total")

    def populate_enneagram_results(self):
        """Populate Enneagram personality types"""
        enneagram_types = [
            "Type 1 - The Perfectionist",
            "Type 2 - The Helper",
            "Type 3 - The Achiever", 
            "Type 4 - The Individualist",
            "Type 5 - The Investigator",
            "Type 6 - The Loyalist",
            "Type 7 - The Enthusiast",
            "Type 8 - The Challenger",
            "Type 9 - The Peacemaker"
        ]
        
        created_count = 0
        for enneagram_type in enneagram_types:
            _, created = EnneagramResult.objects.get_or_create(
                result_name=enneagram_type
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created Enneagram: {enneagram_type}")
        
        self.stdout.write(f"Enneagram Results: {created_count} new, {EnneagramResult.objects.count()} total")

    def populate_gender_identities(self):
        """Populate gender identity options"""
        genders = [
            "Male",
            "Female", 
            "Non-binary",
            "Transgender Male",
            "Transgender Female",
            "Genderfluid",
            "Agender",
            "Other",
            "Prefer not to say"
        ]
        
        created_count = 0
        for gender in genders:
            _, created = GenderIdentity.objects.get_or_create(
                gender=gender
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created Gender Identity: {gender}")
        
        self.stdout.write(f"Gender Identities: {created_count} new, {GenderIdentity.objects.count()} total")

    def populate_osha_types(self):
        """Populate OSHA certification types"""
        osha_types = [
            "OSHA 10-Hour Construction",
            "OSHA 30-Hour Construction", 
            "OSHA 10-Hour General Industry",
            "OSHA 30-Hour General Industry"
        ]
        
        created_count = 0
        for osha_type in osha_types:
            _, created = OshaType.objects.get_or_create(
                name=osha_type
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created OSHA Type: {osha_type}")
        
        self.stdout.write(f"OSHA Types: {created_count} new, {OshaType.objects.count()} total")

    def populate_funding_sources(self):
        """Populate funding source options"""
        funding_sources = [
            "WIOA (Workforce Innovation and Opportunity Act)",
            "Pell Grant",
            "State Grant",
            "Federal Grant",
            "Scholarship",
            "Self-Pay",
            "Employer Sponsored",
            "Trade Adjustment Assistance (TAA)",
            "Veterans Benefits",
            "Other"
        ]
        
        created_count = 0
        for source in funding_sources:
            _, created = FundingSource.objects.get_or_create(
                name=source
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created Funding Source: {source}")
        
        self.stdout.write(f"Funding Sources: {created_count} new, {FundingSource.objects.count()} total")

    def populate_states(self):
        """Populate US states with abbreviations"""
        states_data = [
            ("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AR"), 
            ("California", "CA"), ("Colorado", "CO"), ("Connecticut", "CT"), ("Delaware", "DE"), 
            ("Florida", "FL"), ("Georgia", "GA"), ("Hawaii", "HI"), ("Idaho", "ID"),
            ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"), ("Kansas", "KS"), 
            ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"), ("Maryland", "MD"), 
            ("Massachusetts", "MA"), ("Michigan", "MI"), ("Minnesota", "MN"), ("Mississippi", "MS"), 
            ("Missouri", "MO"), ("Montana", "MT"), ("Nebraska", "NE"), ("Nevada", "NV"),
            ("New Hampshire", "NH"), ("New Jersey", "NJ"), ("New Mexico", "NM"), ("New York", "NY"),
            ("North Carolina", "NC"), ("North Dakota", "ND"), ("Ohio", "OH"), ("Oklahoma", "OK"), 
            ("Oregon", "OR"), ("Pennsylvania", "PA"), ("Rhode Island", "RI"), ("South Carolina", "SC"), 
            ("South Dakota", "SD"), ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"), 
            ("Vermont", "VT"), ("Virginia", "VA"), ("Washington", "WA"), ("West Virginia", "WV"), 
            ("Wisconsin", "WI"), ("Wyoming", "WY")
        ]
        
        created_count = 0
        for state_name, abbreviation in states_data:
            _, created = State.objects.get_or_create(
                name=state_name,
                defaults={'abbreviation': abbreviation}
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created State: {state_name} ({abbreviation})")
        
        self.stdout.write(f"States: {created_count} new, {State.objects.count()} total")

    def populate_regions(self):
        """Populate geographic regions"""
        regions = [
            "Northeast",
            "Southeast", 
            "Midwest",
            "Southwest",
            "West",
            "Pacific",
            "Mountain",
            "Great Lakes",
            "Mid-Atlantic",
            "New England"
        ]
        
        created_count = 0
        for region in regions:
            _, created = Region.objects.get_or_create(
                name=region
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created Region: {region}")
        
        self.stdout.write(f"Regions: {created_count} new, {Region.objects.count()} total")
