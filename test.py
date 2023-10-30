sequence = "00333221222330332033231033120333333203333330323313"
successes = sequence.count('3')
failures = len(sequence) - successes

print(f"Number of successes: {successes}")
print(f"Number of failures: {failures}")
total = len(sequence)
probability_success = successes / total
probability_failure = failures / total

print(f"Probability of success: {probability_success}")
print(f"Probability of failure: {probability_failure}")
