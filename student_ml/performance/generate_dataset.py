"""
Generate a realistic and diverse dataset for student performance prediction.
This creates data that reflects real-world student behaviors and outcomes.
"""
import pandas as pd
import numpy as np

np.random.seed(42)


def calculate_realistic_performance(hours, prev_score, extra, sleep, papers):
    """Calculate performance based on realistic constraints and interactions."""
    
    # Base performance from previous scores (40% weight)
    base = prev_score * 0.4
    
    # Study contribution (30% weight) - diminishing returns after 8 hours
    if hours == 0:
        study_contrib = 0
    elif hours <= 8:
        study_contrib = hours * 3.5
    else:
        study_contrib = 8 * 3.5 + (hours - 8) * 1.5  # Diminishing returns
    
    # Sleep quality multiplier
    if 7 <= sleep <= 9:
        sleep_multiplier = 1.0
    elif 6 <= sleep < 7 or 9 < sleep <= 10:
        sleep_multiplier = 0.9
    elif 5 <= sleep < 6 or 10 < sleep <= 11:
        sleep_multiplier = 0.75
    elif 4 <= sleep < 5:
        sleep_multiplier = 0.6
    elif sleep < 4:
        sleep_multiplier = 0.4
    else:  # > 11 hours
        sleep_multiplier = 0.7
    
    # Practice papers contribution (20% weight)
    practice_contrib = min(papers * 2.5, 20)
    
    # Extracurricular bonus (small but positive)
    extra_bonus = 3 if extra else 0
    
    # Calculate raw performance
    performance = (base + study_contrib * sleep_multiplier + practice_contrib + extra_bonus)
    
    # Apply penalties for extreme cases
    if hours > 12 and sleep < 5:  # Burnout
        performance *= 0.6
    
    if sleep < 3:  # Severe sleep deprivation
        performance *= 0.5
    
    if hours == 0:  # No study
        performance = min(performance, prev_score * 0.6)
    
    # Add some realistic noise
    noise = np.random.normal(0, 2)
    performance += noise
    
    # Realistic bounds
    performance = max(0, min(100, performance))
    
    # Can't improve too much beyond previous score
    max_improvement = prev_score + 25
    if performance > max_improvement:
        performance = max_improvement
    
    return round(performance, 1)


def generate_dataset(n_samples=200):
    """Generate diverse, realistic student data."""
    
    data = []
    
    # Define realistic student profiles
    profiles = [
        # High performers
        {"hours_range": (7, 10), "prev_range": (75, 95), "extra_prob": 0.7, "sleep_range": (6, 9), "papers_range": (5, 10)},
        # Balanced students
        {"hours_range": (4, 7), "prev_range": (60, 80), "extra_prob": 0.6, "sleep_range": (7, 9), "papers_range": (3, 7)},
        # Struggling students
        {"hours_range": (1, 4), "prev_range": (30, 55), "extra_prob": 0.3, "sleep_range": (5, 8), "papers_range": (0, 3)},
        # Burnout risk
        {"hours_range": (10, 14), "prev_range": (65, 85), "extra_prob": 0.2, "sleep_range": (3, 5), "papers_range": (6, 12)},
        # Underachievers (good potential, low effort)
        {"hours_range": (1, 3), "prev_range": (65, 85), "extra_prob": 0.5, "sleep_range": (8, 11), "papers_range": (0, 2)},
        # Sleep deprived
        {"hours_range": (5, 9), "prev_range": (50, 70), "extra_prob": 0.4, "sleep_range": (3, 5), "papers_range": (2, 6)},
        # Oversleepers
        {"hours_range": (2, 5), "prev_range": (40, 65), "extra_prob": 0.3, "sleep_range": (10, 13), "papers_range": (1, 4)},
        # Efficient learners
        {"hours_range": (4, 6), "prev_range": (70, 90), "extra_prob": 0.8, "sleep_range": (7, 9), "papers_range": (4, 8)},
    ]
    
    samples_per_profile = n_samples // len(profiles)
    
    for profile in profiles:
        for _ in range(samples_per_profile):
            hours = np.random.randint(profile["hours_range"][0], profile["hours_range"][1] + 1)
            prev_score = np.random.randint(profile["prev_range"][0], profile["prev_range"][1] + 1)
            extra = np.random.random() < profile["extra_prob"]
            sleep = np.random.randint(profile["sleep_range"][0], profile["sleep_range"][1] + 1)
            papers = np.random.randint(profile["papers_range"][0], profile["papers_range"][1] + 1)
            
            performance = calculate_realistic_performance(hours, prev_score, extra, sleep, papers)
            
            data.append({
                "Hours Studied": hours,
                "Previous Scores": prev_score,
                "Extracurricular Activities": "Yes" if extra else "No",
                "Sleep Hours": sleep,
                "Sample Question Papers Practiced": papers,
                "Performance Index": performance
            })
    
    # Add edge cases
    edge_cases = [
        # No study, no sleep
        (0, 50, "No", 2, 0),
        (0, 60, "Yes", 3, 0),
        # All study, no sleep
        (15, 70, "No", 3, 8),
        (14, 80, "No", 4, 10),
        # Perfect balance
        (7, 85, "Yes", 8, 7),
        (6, 80, "Yes", 8, 6),
        # Excessive sleep
        (2, 55, "No", 14, 1),
        (3, 60, "Yes", 13, 2),
        # High achievers
        (8, 95, "Yes", 8, 10),
        (9, 92, "Yes", 7, 9),
        # Zero effort
        (0, 40, "No", 10, 0),
        (1, 35, "No", 9, 0),
    ]
    
    for hours, prev, extra, sleep, papers in edge_cases:
        extra_bool = extra == "Yes"
        performance = calculate_realistic_performance(hours, prev, extra_bool, sleep, papers)
        data.append({
            "Hours Studied": hours,
            "Previous Scores": prev,
            "Extracurricular Activities": extra,
            "Sleep Hours": sleep,
            "Sample Question Papers Practiced": papers,
            "Performance Index": performance
        })
    
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    print("Generating enhanced dataset...")
    df = generate_dataset(200)
    
    print(f"\nDataset Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"\nPerformance Index range: {df['Performance Index'].min():.1f} - {df['Performance Index'].max():.1f}")
    print(f"Mean performance: {df['Performance Index'].mean():.1f}")
    print(f"\nFeature ranges:")
    print(df.describe())
    
    # Save to CSV
    df.to_csv("dataset.csv", index=False)
    print("\n✓ Enhanced dataset saved to dataset.csv")
