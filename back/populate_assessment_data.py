#!/usr/bin/env python3
"""
Populate production database with personality assessment data
DISC, 16 Personality Types, and Enneagram results
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()

from hammer_backendapi.models import DiscAssessment, SixteenTypeAssessment, EnneagramResult, GenderIdentity, OshaType, FundingSource, State, Region

def populate_disc_assessments():
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
        disc_obj, created = DiscAssessment.objects.get_or_create(
            type_name=disc_type
        )
        if created:
            created_count += 1
            print(f"Created DISC type: {disc_type}")
    
    print(f"DISC Assessments: {created_count} new, {DiscAssessment.objects.count()} total")

def populate_sixteen_types():
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
        type_obj, created = SixteenTypeAssessment.objects.get_or_create(
            type_name=type_name
        )
        if created:
            created_count += 1
            print(f"Created 16 Type: {type_name}")
    
    print(f"16 Personality Types: {created_count} new, {SixteenTypeAssessment.objects.count()} total")

def populate_enneagram_results():
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
        enneagram_obj, created = EnneagramResult.objects.get_or_create(
            result_name=enneagram_type
        )
        if created:
            created_count += 1
            print(f"Created Enneagram: {enneagram_type}")
    
    print(f"Enneagram Results: {created_count} new, {EnneagramResult.objects.count()} total")

def populate_gender_identities():
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
        gender_obj, created = GenderIdentity.objects.get_or_create(
            gender=gender
        )
        if created:
            created_count += 1
            print(f"Created Gender Identity: {gender}")
    
    print(f"Gender Identities: {created_count} new, {GenderIdentity.objects.count()} total")

def populate_osha_types():
    """Populate OSHA certification types"""
    osha_types = [
        "OSHA 10-Hour Construction",
        "OSHA 30-Hour Construction", 
        "OSHA 10-Hour General Industry",
        "OSHA 30-Hour General Industry"
    ]
    
    created_count = 0
    for osha_type in osha_types:
        osha_obj, created = OshaType.objects.get_or_create(
            name=osha_type
        )
        if created:
            created_count += 1
            print(f"Created OSHA Type: {osha_type}")
    
    print(f"OSHA Types: {created_count} new, {OshaType.objects.count()} total")

def populate_funding_sources():
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
        funding_obj, created = FundingSource.objects.get_or_create(
            name=source
        )
        if created:
            created_count += 1
            print(f"Created Funding Source: {source}")
    
    print(f"Funding Sources: {created_count} new, {FundingSource.objects.count()} total")

def populate_states():
    """Populate US states"""
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
        "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York",
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
        "West Virginia", "Wisconsin", "Wyoming"
    ]
    
    created_count = 0
    for state in states:
        state_obj, created = State.objects.get_or_create(
            name=state
        )
        if created:
            created_count += 1
            print(f"Created State: {state}")
    
    print(f"States: {created_count} new, {State.objects.count()} total")

def populate_regions():
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
        region_obj, created = Region.objects.get_or_create(
            name=region
        )
        if created:
            created_count += 1
            print(f"Created Region: {region}")
    
    print(f"Regions: {created_count} new, {Region.objects.count()} total")

def main():
    """Main function to populate all assessment data"""
    print("🔄 Populating production database with assessment data...")
    print("=" * 60)
    
    try:
        populate_disc_assessments()
        print()
        
        populate_sixteen_types()
        print()
        
        populate_enneagram_results()
        print()
        
        populate_gender_identities()
        print()
        
        populate_osha_types()
        print()
        
        populate_funding_sources()
        print()
        
        populate_states()
        print()
        
        populate_regions()
        print()
        
        print("=" * 60)
        print("✅ Successfully populated all assessment data!")
        
    except Exception as e:
        print(f"❌ Error populating data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
