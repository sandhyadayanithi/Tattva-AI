import os
import random
import time
from datetime import datetime, timedelta
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore

# Realistic Claims and Transcripts
FALSE_CLAIMS = [
    {
        "transcript": "My friend told me that drinking papaya leaf juice cures dengue instantly. Doctors are hiding this so please forward it to everyone.",
        "claim": "Papaya leaf juice cures dengue instantly.",
        "category": "health",
        "explanation": "There is no scientific evidence that papaya leaf juice cures dengue. While it may help increase platelet count, it is not a cure and medical supervision is required.",
        "counter_message": "🚩 *FAKE NEWS!* Papaya leaf juice is NOT a cure for dengue. Please consult a doctor immediately if you have symptoms. Stop the spread!",
        "virality_base": 8,
        "virality_reason": "Contains a miraculous cure claim, encourages forwarding, and suggests a conspiracy by doctors."
    },
    {
        "transcript": "Breaking! The Election Commission has announced that those who didn't vote in the last election will have their names removed from the voter list. Check this link now!",
        "claim": "Non-voters will have their names removed from the voter list.",
        "category": "election",
        "explanation": "The Election Commission has no such policy. Voting is a right, not a mandatory requirement for maintaining one's name on the voter list.",
        "counter_message": "❌ *FALSE:* The Election Commission is NOT removing names for not voting. This is a scam to get you to click phishing links. Don't share!",
        "virality_base": 9,
        "virality_reason": "Uses 'Breaking' news framing, creates urgency, and targets civic rights."
    },
    {
        "transcript": "A new investment scheme is giving 50% returns every month. It's backed by the government. Join the WhatsApp group for more details.",
        "claim": "Government-backed investment scheme giving 50% monthly returns.",
        "category": "finance",
        "explanation": "No legitimate government or financial institution offers 50% monthly returns. This is a classic Ponzi scheme pattern.",
        "counter_message": "⚠️ *SCAM ALERT:* High-return schemes are almost always scams. The government does NOT back such plans. Protect your money and don't forward!",
        "virality_base": 7,
        "virality_reason": "Promises easy money and uses fraudulent authority claims."
    },
    {
        "transcript": "A specific temple in the south is giving out a special powder that cures terminal illness. Only available for the next 2 days. Forward this to save lives.",
        "claim": "Special powder from a temple cures terminal illness.",
        "category": "religion",
        "explanation": "Medical conditions require professional treatment. There is no evidence supporting 'miracle powders' as cures for terminal illnesses.",
        "counter_message": "🚫 *FALSE:* Religious faith is important, but miracle powders are not a substitute for medicine. Don't risk lives by spreading this.",
        "virality_base": 9,
        "virality_reason": "High emotional stakes, religious framing, and extreme urgency ('next 2 days')."
    },
    {
        "transcript": "UNESCO has declared the Indian National Anthem as the best in the world. Proud moment for all Indians! Share this everywhere.",
        "claim": "UNESCO declared the Indian National Anthem as the best in the world.",
        "category": "general",
        "explanation": "UNESCO has repeatedly denied making any such declaration. This is a long-standing internet hoax.",
        "counter_message": "🇮🇳 *FACT CHECK:* While we are proud of our anthem, UNESCO has never made such a claim. This is an old hoax. Don't spread misinformation.",
        "virality_base": 6,
        "virality_reason": "Uses national pride and false international authority to encourage sharing."
    }
]

# Add more variations for FALSE_CLAIMS to reach diversity
FALSE_CLAIMS += [
    {
        "transcript": "NASA has confirmed that a massive solar flare will cut off all internet for 10 days starting tomorrow. Stock up on food and water! Forward this!!",
        "claim": "NASA confirmed a 10-day global internet blackout due to solar flares.",
        "category": "general",
        "explanation": "NASA has made no such announcement. While solar flares can affect satellite comms, a total 10-day blackout is unverified and sensationalized.",
        "counter_message": "🛑 *STOP!* NASA has NOT announced an internet blackout. This message is designed to create panic. Don't forward!",
        "virality_base": 10,
        "virality_reason": "Extreme panic-inducing language, clear call to activity, and false agency attribution."
    },
    {
        "transcript": "The government is giving free 5000 rupees to everyone who fills this COVID survey. Link expires in 1 hour. Get yours now!",
        "claim": "Government is giving 5000 rupees for filling a COVID survey.",
        "category": "finance",
        "explanation": "This is a phishing scam. Governments do not collect survey data via WhatsApp links in exchange for cash.",
        "counter_message": "💰 *SCAM:* Do NOT click the link or provide personal info. This is a phishing scam. Warn your friends!",
        "virality_base": 8,
        "virality_reason": "Financial incentive combined with short-lived urgency."
    }
]

TRUE_CLAIMS = [
    {
        "transcript": "The government has announced that the deadline for linking Aadhaar with PAN has been extended to June 30th. Please check the official portal.",
        "claim": "Aadhaar-PAN linking deadline extended to June 30th.",
        "category": "finance",
        "explanation": "The Ministry of Finance regularly updates these deadlines. This information is consistent with official tax department announcements.",
        "virality_base": 3,
        "virality_reason": "Informative and neutral, lacks sensationalism."
    },
    {
        "transcript": "Vaccination is the most effective way to protect yourself and your family from many infectious diseases. Consult your local clinic for the schedule.",
        "claim": "Vaccination protects against infectious diseases.",
        "category": "health",
        "explanation": "Scientific consensus and health organizations like WHO confirm that vaccines are safe and prevent millions of deaths annually.",
        "virality_base": 2,
        "virality_reason": "Fact-based public health information, no emotional manipulation."
    },
    {
        "transcript": "The weather department has issued a red alert for heavy rains in the coastal areas for the next 24 hours. Stay indoors and be safe.",
        "claim": "Red alert issued for heavy rains in coastal areas.",
        "category": "general",
        "explanation": "Official weather bulletins confirm the red alert. It is important to follow state disaster management safety guidelines.",
        "virality_base": 5,
        "virality_reason": "Low to moderate due to practical safety urgency, but lacks conspiracy elements."
    },
    {
        "transcript": "Election Day is March 15th. Make sure you carry your EPIC card to the polling station. Your vote is your voice!",
        "claim": "Election Day is March 15th.",
        "category": "election",
        "explanation": "The dates are as per the official notification from the Election Commission of India for the current cycle.",
        "virality_base": 4,
        "virality_reason": "Civic awareness, neutral tone."
    }
]

LANGUAGES = ["Tamil", "Hindi", "Telugu", "Bengali", "English"]

def seed_data():
    # 1. Initialize Firebase
    from config.firebase_config import db
    if db is None:
        print("Error: Could not initialize Firestore. Check service_account.json.")
        return

    # 2. Check for Idempotency
    print("Checking for existing seed...")
    flag_ref = db.collection("system_flags").document("seed_initialized")
    if flag_ref.get().exists:
        print("Firestore already seeded. Skipping generation.")
        return

    # 3. Generate Records
    record_count = random.randint(80, 120)
    print(f"Generating {record_count} simulated records...")

    batch = db.batch()
    now = datetime.now()

    for i in range(record_count):
        # Decide TRUE or FALSE
        is_false = random.choice([True, False, True]) # Slightly more false claims for the demo
        
        if is_false:
            source = random.choice(FALSE_CLAIMS)
            verdict = "FALSE"
        else:
            source = random.choice(TRUE_CLAIMS)
            verdict = "TRUE"

        # Randomize items slightly
        virality_score = min(10, max(1, source["virality_base"] + random.randint(-1, 1)))
        
        # Random language
        lang = random.choice(LANGUAGES)
        
        # Random timestamp within last 24h
        created_at = now - timedelta(minutes=random.randint(0, 1440))
        
        record = {
            "transcript": source["transcript"],
            "claim": source["claim"],
            "verdict": verdict,
            "explanation": source["explanation"],
            "virality_score": virality_score,
            "virality_reason": source["virality_reason"],
            "counter_message": source.get("counter_message") if verdict == "FALSE" else None,
            "language": lang,
            "category": source["category"],
            "created_at": created_at
        }

        doc_ref = db.collection("fact_checks").document()
        batch.set(doc_ref, record)

        if (i + 1) % 20 == 0:
            print(f"  Prepared {i + 1} records...")

    # commit batch
    print("Committing batch to Firestore...")
    batch.commit()

    # 4. Set Flag
    flag_ref.set({
        "initialized_at": firestore.SERVER_TIMESTAMP,
        "record_count": record_count
    })

    print(f"SUCCESS: Successfully created {record_count} records in 'fact_checks'.")

if __name__ == "__main__":
    seed_data()
