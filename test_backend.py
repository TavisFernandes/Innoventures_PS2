import sys
import os

# Add the Backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'Backend')
sys.path.insert(0, backend_path)

from main import PDFQASystem

def main():
    print(">> Initializing PlugMind AI Backend...")
    print("   Loading ML Models, parsing PDFs, and initializing AI connections (Gemini/Llama).")
    
    # Initialize the core backend system
    qa_system = PDFQASystem()

    print("\n" + "="*50)
    print("💼 PLUGMIND FINANCE EXPERT - BACKEND TERMINAL")
    print("="*50)

    while True:
        print("\nOptions:")
        print("1. Ask a Finance Question")
        print("2. Test Loan Eligibility Prediction")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            question = input("\n📝 Enter your finance question: ")
            if question.strip():
                print("\n🤔 Analyzing with Documents + Gemini/Llama...\n")
                
                # The backend handles routing to the Finance Expert plugin, parsing PDFs/CSVs, 
                # calculating the Confidence Score, and contacting Gemini or Llama natively.
                answer = qa_system.answer_question(question.strip())
                
                print("-" * 50)
                print("📋 RAW BACKEND RESPONSE:")
                print("-" * 50)
                print(answer)
                print("-" * 50)
                
        elif choice == '2':
            print("\n🎯 Initiating Loan Prediction Test")
            print("   Using default test constraints to trigger ML pipeline...")
            
            # Simulated incoming applicant data
            applicant_data = {
                'Gender': 'Female',
                'Married': 'No',
                'Dependents': '0',
                'Education': 'Graduate',
                'Self_Employed': 'No',
                'ApplicantIncome': 8500,
                'CoapplicantIncome': 0,
                'LoanAmount': 200,
                'Loan_Amount_Term': 360,
                'Credit_History': 1.0,
                'Property_Area': 'Urban'
            }
            
            prediction, probability, explanation = qa_system.predict_loan_eligibility(applicant_data)
            
            print("-" * 50)
            print("🔮 RAW PREDICTION OUTPUT:")
            print("-" * 50)
            print(explanation)
            print("-" * 50)
            
        elif choice == '3' or choice.lower() in ('q', 'quit', 'exit'):
            print("\nShutting down backend session...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
