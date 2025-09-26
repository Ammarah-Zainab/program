import json
import random
from datetime import datetime

# File to save flashcards
FLASHCARD_FILE = "flashcards.json"

# Load existing flashcards from file (if available)
try:
    with open(FLASHCARD_FILE, "r") as file:
        flashcards = json.load(file)
except FileNotFoundError:
    flashcards = []

# Function to save flashcards to the file
def save_flashcards():
    with open(FLASHCARD_FILE, "w") as file:
        json.dump(flashcards, file, indent=4)

print("=== Flashcard Quiz Program ===")

while True:
    print("\nMenu:")
    print("1. Add a Flashcard")
    print("2. View All Flashcards")
    print("3. Quiz Yourself")
    print("4. Search Flashcard")
    print("5. Delete Flashcard")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ").strip()

    if choice == "1":
        # Add a flashcard
        question = input("Enter the question: ").strip()
        answer = input("Enter the answer: ").strip()
        category = input("Enter the category (e.g., Math, Science, IQ): ").strip()
        flashcards.append({
            "id": len(flashcards) + 1,
            "question": question,
            "answer": answer,
            "category": category,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "times_correct": 0,
            "times_wrong": 0
        })
        save_flashcards()
        print(f"Flashcard added in '{category}' category!")

    elif choice == "2":
        # View all flashcards
        if flashcards:
            print(f"\n--- Flashcards List (Total: {len(flashcards)}) ---")
            for card in flashcards:
                print(f"ID: {card['id']} | Q: {card['question']} | A: {card['answer']} | Category: {card['category']}")
        else:
            print("\nNo flashcards available.")

    elif choice == "3":
        # Quiz mode
        if not flashcards:
            print("\nNo flashcards to quiz.")
        else:
            print("\n--- Quiz Mode ---")
            categories = list(set(card["category"] for card in flashcards))
            print("Available categories:", ", ".join(categories))
            category_choice = input("Enter category name or 'all' for all categories: ").strip()

            if category_choice.lower() == "all":
                quiz_cards = flashcards[:]
            else:
                quiz_cards = [card for card in flashcards if card["category"].lower() == category_choice.lower()]

            if not quiz_cards:
                print("No flashcards found in that category.")
                continue

            try:
                num = int(input(f"How many questions do you want? (max {len(quiz_cards)}): "))
            except ValueError:
                print("Invalid input. Enter a number.")
                continue

            if num <= 0 or num > len(quiz_cards):
                print("Invalid number of questions.")
                continue

            quiz_cards = random.sample(quiz_cards, num)
            correct = 0
            wrong = 0

            for card in quiz_cards:
                print(f"\nQuestion: {card['question']}")
                user_ans = input("Your Answer: ").strip()
                if user_ans.lower() == card['answer'].lower():
                    print("Correct!")
                    card['times_correct'] += 1
                    correct += 1
                else:
                    print(f"Wrong! Correct answer: {card['answer']}")
                    card['times_wrong'] += 1
                    wrong += 1

            save_flashcards()
            print(f"\nQuiz completed! Score: {correct} correct, {wrong} wrong.\n")

    elif choice == "4":
        # Search for a flashcard
        search_term = input("Enter keyword to search: ").strip().lower()
        found = False
        for card in flashcards:
            if search_term in card['question'].lower() or search_term in card['answer'].lower():
                print(f"\nFound: ID {card['id']} | Q: {card['question']} | A: {card['answer']} | Category: {card['category']}")
                found = True
        if not found:
            print("No flashcards found for your search.")

    elif choice == "5":
        # Delete a flashcard
        delete_id = input("Enter ID of flashcard to delete: ").strip()
        if delete_id.isdigit():
            delete_id = int(delete_id)
            for card in flashcards:
                if card['id'] == delete_id:
                    flashcards.remove(card)
                    save_flashcards()
                    print(f"Flashcard ID {delete_id} deleted successfully!")
                    break
            else:
                print("Flashcard ID not found.")
        else:
            print("Invalid ID entered.")

    elif choice == "6":
        # Exit program
        print("\nExiting Flashcard Quiz Program... Goodbye!")
        break

    else:
        print("Invalid choice! Please select from 1 to 6.")