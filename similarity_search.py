
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import spacy
import re
from sentence_transformers import SentenceTransformer
from nltk.corpus import wordnet
from collections import defaultdict
import torch
from typing import List, Dict, Any
import logging
import json



ai_engineer_skills = [
    "Python Programming",
    "Machine Learning Algorithms",
    "Deep Learning (CNNs, RNNs, Transformers)",
    "Data Structures & Algorithms",
    "Mathematics for AI (Linear Algebra, Calculus, Probability, Statistics)",
    "Model Training & Evaluation (Accuracy, Precision, Recall, F1-score)",
    "Data Preprocessing & Cleaning",
    "Natural Language Processing (NLP)",
    "Computer Vision",
    "AI Frameworks & Libraries (TensorFlow, PyTorch, Scikit-learn, Keras)",
    "Version Control (Git & GitHub)",
    "Cloud Platforms (AWS, GCP, Azure)",
    "Model Deployment (APIs, Flask/FastAPI, Docker)",
]

def preprocess_text(text):
    """Clean and standardize text data"""
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^\w\s]', ' ', str(text).lower())
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def load_courses():
    # Read the CSV file
    df = pd.read_csv('courses_courses.csv')
    # Clean the text data
    df['title'] = df['title'].apply(preprocess_text)
    df['description'] = df['description'].apply(preprocess_text)
    # Combine title and description with more weight on title
    df['combined_text'] = df['title'] + ' ' + df['title'] + ' ' + df['description']
    return df

class CourseSkillMatcher:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize with BERT-based sentence transformer and other components"""
        self.sentence_transformer = SentenceTransformer(model_name)
        self.nlp = spacy.load('en_core_web_sm')
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for tracking matching process"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def get_wordnet_synonyms(self, word: str) -> set:
        """Get synonyms for a word using WordNet"""
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower().replace('_', ' '))
        return synonyms

    def enhance_skills(self, skills: List[str]) -> List[str]:
        """Enhance skills with synonyms and related terms"""
        enhanced_skills = []
        for skill in skills:
            skill_terms = {skill.lower()}
            
            # Add WordNet synonyms
            words = skill.lower().split()
            for word in words:
                skill_terms.update(self.get_wordnet_synonyms(word))
            
            # Add spaCy variations
            doc = self.nlp(skill.lower())
            skill_terms.update([token.lemma_ for token in doc])
            
            enhanced_skills.append(' '.join(skill_terms))
        return enhanced_skills

    def create_course_embeddings(self, courses_df: pd.DataFrame) -> torch.Tensor:
        """Create and cache BERT embeddings for courses"""
        self.logger.info("Generating course embeddings...")
        
        # Combine title and description with weights
        weighted_texts = [
            f"{row['title']} {row['title']} {row['description']}"
            for _, row in courses_df.iterrows()
        ]
        
        # Force CPU usage
        return self.sentence_transformer.encode(
            weighted_texts,
            convert_to_tensor=True,
            show_progress_bar=True,
            device='cpu'  # Force CPU usage
        )

    def calculate_similarity_scores(
        self,
        course_embeddings: torch.Tensor,
        skill_embeddings: torch.Tensor
    ) -> np.ndarray:
        """Calculate similarity using multiple metrics"""
        # Cosine similarity
        cosine_scores = torch.nn.functional.cosine_similarity(
            skill_embeddings.unsqueeze(1),
            course_embeddings.unsqueeze(0),
            dim=2
        ).numpy().astype(float)  # Convert to native Python float
        
        return cosine_scores

    def analyze_course_content(self, course_text: str, skill: str) -> Dict[str, Any]:
        """Detailed analysis of course content"""
        doc = self.nlp(course_text)
        
        analysis = {
            'key_concepts': [],
            'technical_terms': [],
            'skill_mentions': 0,
            'complexity_score': 0
        }
        
        # Extract key concepts and technical terms
        for ent in doc.ents:
            if ent.label_ in ['TECH', 'PRODUCT', 'ORG']:
                analysis['technical_terms'].append(ent.text)
            
        # Count skill-related terms
        skill_terms = set(skill.lower().split())
        analysis['skill_mentions'] = sum(
            1 for token in doc if token.text.lower() in skill_terms
        )
        
        # Calculate complexity score based on technical density
        analysis['complexity_score'] = len(analysis['technical_terms']) / len(doc)
        
        return analysis

    def find_best_courses(
        self,
        courses_df: pd.DataFrame,
        skills: List[str],
        top_n: int = 3,
        threshold: float = 0.1
    ) -> List[Dict]:
        """Enhanced course matching with detailed analysis"""
        self.logger.info(f"Starting course matching for {len(skills)} skills...")
        
        # Enhance skills with related terms
        enhanced_skills = self.enhance_skills(skills)
        
        # Generate embeddings
        course_embeddings = self.create_course_embeddings(courses_df)
        skill_embeddings = self.sentence_transformer.encode(
            enhanced_skills,
            convert_to_tensor=True
        )
        
        # Calculate similarity scores
        similarity_matrix = self.calculate_similarity_scores(
            course_embeddings,
            skill_embeddings
        )
        
        results = []
        for i, skill in enumerate(skills):
            course_scores = similarity_matrix[i]
            valid_indices = np.where(course_scores >= threshold)[0]
            
            matches = []
            for idx in valid_indices:
                course_row = courses_df.iloc[idx]
                score = course_scores[idx]
                
                # Detailed course analysis
                analysis = self.analyze_course_content(
                    f"{course_row['title']} {course_row['description']}",
                    skill
                )
                
                # Calculate confidence level with multiple factors
                confidence_score = (
                    score * 0.5 +
                    min(analysis['skill_mentions'] * 0.1, 0.3) +
                    min(analysis['complexity_score'] * 0.2, 0.2)
                )
                
                confidence_level = (
                    "High" if confidence_score > 0.7
                    else "Medium" if confidence_score > 0.4
                    else "Low"
                )
                
                matches.append({
                    'course': course_row['title'],
                    'score': score,
                    'confidence': confidence_level,
                    'analysis': analysis,
                    'description': course_row['description']
                })
            
            # Sort by score and take top N
            matches.sort(key=lambda x: x['score'], reverse=True)
            results.append({
                'skill': skill,
                'matching_courses': matches[:top_n]
            })
            
        return results

    def save_results(self, results: List[Dict], filepath: str):
        """Save matching results to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)

# Main execution
if __name__ == "__main__":
    matcher = CourseSkillMatcher()
    courses_df = load_courses()
    results = matcher.find_best_courses(courses_df, ai_engineer_skills)
    
    # Save results
    matcher.save_results(results, 'course_matches.json')
    
    # Print detailed results
    for result in results:
        print(f"\nSkill: {result['skill']}")
        print("Matching Courses:")
        for course in result['matching_courses']:
            print(f"\n- {course['course']}")
            print(f"  Confidence: {course['confidence']}")
            print(f"  Score: {course['score']:.3f}")
            print(f"  Technical Terms: {', '.join(course['analysis']['technical_terms'])}")
            print(f"  Complexity Score: {course['analysis']['complexity_score']:.2f}")
            print(f"  Skill Mentions: {course['analysis']['skill_mentions']}")




