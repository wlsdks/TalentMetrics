import streamlit as st

def render_footer():
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-logo">
                <i class="fas fa-chart-line"></i> TalentMetrics
            </div>
            <p class="footer-copyright">© 2025 TalentMetrics - HR 채용 대시보드 v2.0</p>
            <p class="footer-tagline">데이터 기반의 스마트한 채용 의사결정을 위한 솔루션</p>
            <div class="footer-links">
                <a href="#" class="footer-link"><i class="fas fa-book"></i> 문서</a>
                <a href="#" class="footer-link"><i class="fas fa-envelope"></i> 문의하기</a>
                <a href="#" class="footer-link"><i class="fas fa-code"></i> GitHub</a>
            </div>
        </div>
    </div>
    <style>
        .footer {
            text-align: center;
            padding: 2.5rem 0;
            color: var(--neutral-500, #737373);
            font-size: 0.95rem;
            border-top: 1px solid var(--neutral-200, #e5e5e5);
            margin-top: 4rem;
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .footer-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .footer-logo {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--primary-600, #4f46e5);
            margin-bottom: 0.75rem;
        }
        
        .footer-logo i {
            margin-right: 0.5rem;
        }
        
        .footer-copyright {
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .footer-tagline {
            font-size: 0.875rem;
            color: var(--neutral-400, #a3a3a3);
            margin-bottom: 1.5rem;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-top: 1rem;
        }
        
        .footer-link {
            color: var(--primary-600, #4f46e5);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.875rem;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            transition: background-color 0.3s, color 0.3s;
        }
        
        .footer-link:hover {
            background-color: var(--primary-50, #eef2ff);
            color: var(--primary-700, #4338ca);
        }
        
        .footer-link i {
            margin-right: 0.375rem;
        }
        
        @media (prefers-color-scheme: dark) {
            .footer {
                background-color: var(--neutral-800, #262626);
                border-top-color: var(--neutral-700, #404040);
            }
            
            .footer-link:hover {
                background-color: var(--neutral-700, #404040);
            }
        }
        
        @media screen and (max-width: 768px) {
            .footer-links {
                flex-direction: column;
                gap: 0.75rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)