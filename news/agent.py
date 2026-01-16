import os
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

# Load environment variables
load_dotenv()

class NewsAgent:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun()
    
    def needs_real_time_info(self, query):
        query_lower = query.lower()
        
        no_search_queries = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon',
            'who are you', 'what are you', 'your name', 'help',
            'thank you', 'thanks', 'bye', 'goodbye'
        ]
        
        if query_lower.strip() in [phrase.strip() for phrase in no_search_queries]:
            return False
        
        general_knowledge_starters = [
            'what is', 'who is', 'define', 'explain', 'meaning of',
            'difference between', 'how to', 'why is'
        ]
        
        for starter in general_knowledge_starters:
            if query_lower.startswith(starter):
                current_keywords = ['current', 'latest', 'today', 'now', 'recent', 'new']
                if any(keyword in query_lower for keyword in current_keywords):
                    return True
                return False
        
        return True
    
    def generate_response(self, query):
        query = query.strip()
        query_lower = query.lower()
        
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if query_lower in greetings:
            return "👋 **Hello!** I'm your AI News Agent. I can search for real-time news and information for you!"
        
        if query_lower == 'help' or query_lower == 'help me':
            return "🆘 **Help:** I can help you find current news and information. Ask me about any topic, and I'll search the web for latest updates!"
        
        if query_lower in ['who are you', 'what are you', 'your name']:
            return "🤖 **About Me:** I'm an AI-powered Real-Time News Agent. I search the web for current information!"
        
        if not self.needs_real_time_info(query):
            return f"""🧠 **General Knowledge Response**

📝 **Your Query:** {query}

💡 **Response:** This appears to be a general knowledge question. While I focus on real-time information, here's what I understand:

For the most accurate and current information, please include words like:
• **'latest'** 
• **'today'** 
• **'current'** 
• **'recent'** 
• **'now'**

**Example:** Instead of "weather", try "weather today" or "current weather forecast"."""
        
        try:
            print(f"🔍 Searching for: {query}")
            
            clean_query = query.replace('?', '').strip()
            
            # Try multiple search variations for better results
            search_variations = [
                f"{clean_query} latest news 2024",
                f"{clean_query} today news update",
                f"current {clean_query} news",
                clean_query
            ]
            
            search_results = ""
            for search_query in search_variations:
                results = self.search_tool.run(search_query)
                if results and len(results.strip()) > 100:
                    search_results = results
                    break
            
            if not search_results or len(search_results.strip()) < 50:
                return f"""🔍 **Search Report**

📋 **Query:** {query}
⚠️ **Status:** Limited information found

💡 **Suggestions for better results:**
• **Be specific** - Instead of "news", try "technology news" or "sports news"
• **Add time frame** - Include "today", "this week", or "latest"
• **Check spelling** - Verify any names or technical terms
• **Try related topics** - Sometimes broader or narrower queries work better

📌 **Example:** "Odisha political news today" instead of "odisha news" """
            
            import re
            
            # Clean the text
            cleaned_text = search_results
            
            # Remove short fragments and duplicates
            sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
            unique_sentences = []
            seen_sentences = set()
            
            for sentence in sentences:
                sentence = sentence.strip()
                # Keep only meaningful sentences (at least 20 chars)
                if len(sentence) > 20 and sentence.lower() not in seen_sentences:
                    # Remove common useless patterns
                    if not any(pattern in sentence.lower() for pattern in [
                        'click here', 'read more', 'continue reading',
                        'for more', 'share this', 'related articles',
                        '...', 'watch video', 'photo gallery',
                        'test your news', 'catch up on'
                    ]):
                        unique_sentences.append(sentence)
                        seen_sentences.add(sentence.lower())
            
            # Take the most relevant sentences (up to 10)
            relevant_sentences = unique_sentences[:10]
            
            # Format the response
            response = "📡 **AI NEWS AGENT REPORT**\n\n"
            response += f"🔎 **Query:** {query}\n"
            response += f"🕒 **Time:** Latest Information\n\n"
            response += "────────────────────────────────────────\n\n"
            
            if relevant_sentences:
                response += "📰 **LATEST UPDATES:**\n\n"
                for i, sentence in enumerate(relevant_sentences, 1):
                    # Ensure proper ending
                    if not sentence.endswith(('.', '!', '?')):
                        sentence += '.'
                    response += f"{i}. {sentence}\n\n"
            else:
                # Fallback: show first 500 characters of cleaned text
                response += "📋 **SUMMARY:**\n\n"
                summary = cleaned_text[:600]
                if len(cleaned_text) > 600:
                    summary += "..."
                response += f"{summary}\n\n"
            
            response += "────────────────────────────────────────\n"
            response += "📊 **Report Info:**\n"
            response += "• Source: Real-time web search\n"
            response += "• Type: Current information\n"
            response += "• Status: Live data compiled\n\n"
            response += "════════════════════════════════════════"
            
            return response
            
        except Exception as e:
            print(f"Error: {e}")
            return f"""⚠️ **System Notice**

🔄 **Issue:** Technical difficulty encountered

🔧 **Action:** Please try again in a moment

📞 **Status:** Service temporarily unavailable"""