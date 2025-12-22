
# DERS NOTU ANALİZ ASİSTANI - STREAMLIT 

import os
import streamlit as st
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge import Knowledge
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.embedder.ollama import OllamaEmbedder

# Sayfa Ayarları
st.set_page_config(
    page_title="🎓 Ders Notu Asistanı",
    page_icon="📚",
    layout="wide"
)

st.title("🎓 Ders Notu Analiz Asistanı")
st.markdown("---")

# ==============================
# SİSTEM BAŞLATMA
# ==============================

@st.cache_resource
def initialize_system():
    """Sistem bileşenlerini başlat (sadece bir kez çalışır)"""
    
    with st.spinner("🔧 Sistem başlatılıyor..."):
        
        # 1. Veritabanı Bağlantısı
        st.info("📊 Veritabanına bağlanılıyor...")
        try:
            vector_db = Qdrant(
                collection="ders_notlari",
                url="http://localhost:6333",
                embedder=OllamaEmbedder(id="openhermes")
            )
            st.success("✅ Veritabanı hazır!")
        except Exception as e:
            st.error(f"❌ Veritabanı hatası: {e}")
            st.info("💡 Docker çalışıyor mu kontrol et: `docker ps`")
            st.stop()
        
        # 2. Bilgi Tabanı Oluştur
        st.info("📚 Bilgi tabanı oluşturuluyor...")
        try:
            knowledge_base = Knowledge(
                vector_db=vector_db
            )
            st.success("✅ Bilgi tabanı hazır!")
        except Exception as e:
            st.error(f"❌ Bilgi tabanı hatası: {e}")
            st.stop()
        
        # 3. PDF'leri Kontrol Et
        documents_path = "documents"
        
        if not os.path.exists(documents_path):
            st.error("❌ 'documents' klasörü bulunamadı!")
            st.stop()
        
        pdf_files = [f for f in os.listdir(documents_path) if f.endswith('.pdf')]
        
        if len(pdf_files) == 0:
            st.warning("⚠️ 'documents' klasöründe PDF bulunamadı!")
            st.info("💡 PDF ders notlarını 'documents' klasörüne ekleyin")
            st.stop()
        
        st.info(f"📄 {len(pdf_files)} PDF bulundu")
        
        # 4. PDF'leri Yükle
        st.info("🔄 PDF'ler yükleniyor ve analiz ediliyor...")
        try:
            progress_bar = st.progress(0)
            for idx, pdf_file in enumerate(pdf_files):
                pdf_path = os.path.join(documents_path, pdf_file)
                # PDF'i bilgi tabanına ekle
                knowledge_base.add_content(pdf_path)
                # İlerleme çubuğunu güncelle
                progress_bar.progress((idx + 1) / len(pdf_files))
            
            st.success(f"✅ {len(pdf_files)} PDF başarıyla yüklendi!")
        except Exception as e:
            st.error(f"❌ PDF yükleme hatası: {e}")
            st.code(str(e))
            st.stop()
        
        # 5. AI Asistanı Oluştur
        st.info("🤖 AI Asistanı hazırlanıyor...")
        try:
            agent = Agent(
                name="Ders Notu Asistanı",
                model=Ollama(id="llama3.2"),
                knowledge=knowledge_base,
                description="""
                Sen bir ders notu analiz asistanısın. 
                Öğrencilerin ders notlarıyla ilgili sorularını cevaplıyorsun.
                Hangi konunun hangi notta olduğunu söyleyebilirsin.
                """,
                instructions=[
                    "Soruları sadece yüklenen ders notlarına dayanarak cevapla",
                    "Hangi PDF dosyasından bilgi aldığını belirt",
                    "Açık ve anlaşılır Türkçe kullan",
                    "Eğer notta yoksa 'Bu bilgi notlarda yok' de",
                ],
                markdown=True,
            )
            st.success("✅ Asistan hazır!")
            return agent
            
        except Exception as e:
            st.error(f"❌ Asistan oluşturma hatası: {e}")
            st.info("💡 Ollama çalışıyor mu kontrol et: `ollama list`")
            st.stop()

# Sistemi Başlat
agent = initialize_system()

st.markdown("---")
st.markdown("### 💬 Asistanınıza Soru Sorun")

# ==============================
# CHAT ARAYÜZÜ
# ==============================

# Chat geçmişi için session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Önceki mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı inputu
if prompt := st.chat_input("Sorunuzu yazın... (örn: 'Python'da döngü nedir?')"):
    
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Asistan cevabı
    with st.chat_message("assistant"):
        with st.spinner("🤔 Düşünüyorum..."):
            try:
                # Ajanı çalıştır
                response = agent.run(prompt)
                
                # Cevabı al
                if hasattr(response, 'content'):
                    answer = response.content
                elif isinstance(response, str):
                    answer = response
                else:
                    answer = str(response)
                
                # Cevabı göster
                st.markdown(answer)
                
                # Geçmişe kaydet
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer
                })
                
            except Exception as e:
                error_msg = f"❌ Bir hata oluştu: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# ==============================
# YAN PANEL - BİLGİLER
# ==============================
with st.sidebar:
    st.header("📖 Kullanım Kılavuzu")
    
    st.markdown("""
    **Örnek Sorular:**
    - "Hangi konular var?"
    - "Python'da döngü nedir?"
    - "Bölüm 3'te ne anlatılıyor?"
    - "Fonksiyonları açıkla"
    - "Liste ve tuple farkı nedir?"
    """)
    
    st.markdown("---")
    
    st.markdown("**⚙️ Sistem Durumu:**")
    st.success("✅ Qdrant Aktif")
    st.success("✅ Ollama Aktif")
    st.success("✅ PDF'ler Yüklü")
    
    st.markdown("---")
    
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")

