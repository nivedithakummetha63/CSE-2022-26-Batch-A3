from .models import Preferences

# 🔢 Fields used for similarity calculation
SIMILAR_FIELDS = [
    'bedtime','cleanliness','noise_tolerance','guest_frequency',
    'smoking','alcohol','food_type','personality','pet_tolerance',
    'education_level','group_study','study_importance','study_habits',
    'phone_calls','language','sharing_belongings','privacy'
]

# 🔴 STEP 2: Mandatory filter
def mandatory_filter(user_pref):
    qs = Preferences.objects.exclude(user=user_pref.user)

    if user_pref.gender != 'Any':
        qs = qs.filter(user__profile__gender=user_pref.gender)

    qs = qs.filter(
        room_sharing=user_pref.room_sharing,
        ac_preference=user_pref.ac_preference
    )

    return qs


# 🟡 STEP 3: Similarity score
def similarity_score(p1, p2):
    score = 0
    for field in SIMILAR_FIELDS:
        if getattr(p1, field) == getattr(p2, field):
            score += 1

    return round((score / len(SIMILAR_FIELDS)) * 100, 2)


# 🔵 STEP 4: Final match engine
def find_best_matches(user):
    user_pref = Preferences.objects.get(user=user)

    mandatory_matches = mandatory_filter(user_pref)

    scored = []
    for pref in mandatory_matches:
        score = similarity_score(user_pref, pref)
        scored.append((pref, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    strong_matches = [m for m in scored if m[1] >= 60][:5]

    if strong_matches:
        return strong_matches

    if scored:
        return scored[:5]

    return []
