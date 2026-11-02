import os
import re

from dotenv import load_dotenv

load_dotenv()

try:
    from groq import Groq
except ImportError:
    Groq = None


class ProfessionalChatbot:
    """PROFESSIONAL Chatbot - CartScout Optimized"""
    
    def __init__(self, products_data):
        # API Key environment variable
        # Without a key (or the groq package) the assistant still handles greetings,
        # the off-topic guardrail and direct product lookups; only the LLM fallback is off.
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key) if (api_key and Groq) else None
        self.products = products_data
        self.conversation = []
        self.build_index()
        self.categories_list = list(set([p['category'] for p in products_data]))
    
    def build_index(self):
        self.product_index = {}
        for p in self.products:
            self.product_index[p['name'].lower()] = p
            self.product_index[p['brand'].lower()] = p
            if 'tags' in p:
                for tag in p['tags']:
                    self.product_index[tag.lower()] = p
    
    def find_product(self, query):
        q = query.lower().strip()
        # Direct lookup
        if q in self.product_index:
            return self.product_index[q]
        # Partial match
        for p in self.products:
            if q in p['name'].lower() or q in p['brand'].lower():
                return p
        return None

    def format_product(self, p):
        reviews = "\n".join([f"  • {r}" for r in p.get('reviews', [])[:2]])
        return f"""✅ **{p['name']}**
Brand: {p['brand']} | Price: ${p['price']:,.2f} | ⭐ {p['rating']}/5
Status: {'In Stock' if p['in_stock'] else 'Out of Stock'}
Advice: This product is highly popular due to its quality and the reliability of {p['brand']}.
Reviews:
{reviews}"""

    def chat(self, user_message):
        if not user_message.strip():
            return "Please type something!"
        
        u_msg = user_message.lower().strip()

        # 1. GREETINGS (Ab yeh sab se pehle check hoga)
        greetings = ['hi', 'hello', 'hey', 'salam', 'aoa', 'how are you', 'kaise ho', 'hy']
        
        # Agar user ka message chota hai aur usme koi greeting word hai
        if any(re.search(rf'\b{re.escape(greet)}\b', u_msg) for greet in greetings) and len(u_msg) < 15:
            return "Hello! I am your CartScout assistant. How can I help you find the perfect product today? I can give you advice on our Electronics and Fashion collections!"

        # 2. STRICT GUARDRAIL (Politics, News, etc.)
        # Yeh tab chalega agar message greeting nahi hai
        forbidden_topics = ['politics', 'election', 'war', 'news', 'prime minister', 'president', 'religion', 'ipl', 'cricket', 'weather']
        if any(re.search(rf'\b{re.escape(topic)}\b', u_msg) for topic in forbidden_topics):
            return "Sorry!! You can only ask me about shopping or shopping-related things."
        
        # 3. PRODUCT CHECK
        product = self.find_product(u_msg)
        if product:
            response = self.format_product(product)
            # Memory update
            self.conversation.append({"role": "user", "content": user_message})
            self.conversation.append({"role": "assistant", "content": response})
            return response

        # 4. LLM LOGIC (For advice and out-of-stock handling)
        # Context building for Groq
        system_instruction = f"""
        You are a professional Shopping Assistant. 
        - Current Inventory Categories: {', '.join(self.categories_list)}.
        - If user asks for advice or a product NOT in inventory, say: "Sorry, we don't have this product right now but we will work on this soon! Would you like to see our other products?"
        - If they ask for general shopping advice (e.g., 'Which brand is better?'), provide a helpful comparison but keep it professional.
        - NEVER talk about anything other than shopping. If they try to deviate, say: "I can only assist you with shopping related queries."
        1. Default Language: Always start in English.
        2. User Preference: If the user speaks in Roman Urdu (e.g., "kaise ho", "kya haal hai"), respond in Roman Urdu
        3.Dont used hindi words (i.e vikalyp)"""

        if self.client is None:
            return ("The AI advice feature is switched off (no GROQ_API_KEY configured). "
                    "You can still search for a product by name, brand or tag.")

        try:
            # Add user msg to memory
            current_chat = [{"role": "user", "content": user_message}]
            
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": system_instruction}] + self.conversation + current_chat,
                max_tokens=150,
                temperature=0.5 # Lower temperature for more focused answers
            )
            
            response = completion.choices[0].message.content
            self.conversation.append({"role": "user", "content": user_message})
            self.conversation.append({"role": "assistant", "content": response})
            return response

        except Exception as e:
            return "I'm sorry, I'm having trouble connecting. But generally, we deal in Electronics and Fashion. Could you ask about those?"

    def reset(self):
        self.conversation = []