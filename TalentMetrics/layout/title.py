import streamlit as st

def render_title():
    st.markdown("""
    <div class="header-container">
        <div class="header-icon">
            <i class="fas fa-chart-line"></i>
        </div>
        <div class="header-content">
            <div class="main-title">TalentMetrics</div>
            <div class="sub-title">채용 데이터를 시각화하고 핵심 인사이트를 발견하세요</div>
        </div>
        <div class="header-accent">
            <svg width="150" height="120" viewBox="0 0 150 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="130" cy="20" r="80" fill="rgba(255, 255, 255, 0.05)"/>
                <circle cx="140" cy="10" r="60" fill="rgba(255, 255, 255, 0.03)"/>
                <circle cx="125" cy="30" r="40" fill="rgba(255, 255, 255, 0.02)"/>
            </svg>
        </div>
    </div>
    <style>
        .header-container {
            background: linear-gradient(120deg, var(--primary-600, #4f46e5), var(--primary-800, #3730a3));
            color: white;
            padding: 1.75rem 2rem;
            border-radius: 0.75rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
        }
        
        .header-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            transform: rotate(30deg);
            z-index: 1;
        }
        
        .header-content {
            position: relative;
            z-index: 2;
            flex-grow: 1;
        }
        
        .header-icon {
            font-size: 2.5rem;
            margin-right: 1.5rem;
            color: rgba(255, 255, 255, 0.9);
            background: rgba(255, 255, 255, 0.1);
            width: 4.5rem;
            height: 4.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
            animation: pulse 3s infinite ease-in-out;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
            line-height: 1.2;
            background: linear-gradient(to right, white, rgba(255, 255, 255, 0.8));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .sub-title {
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 0;
            font-weight: 400;
            letter-spacing: -0.01em;
        }
        
        .header-accent {
            position: absolute;
            right: 0;
            top: 0;
            z-index: 1;
            opacity: 0.3;
            pointer-events: none;
        }
        
        @media screen and (max-width: 768px) {
            .header-container {
                padding: 1.25rem;
                flex-direction: column;
                text-align: center;
            }
            
            .header-icon {
                margin-right: 0;
                margin-bottom: 1rem;
                width: 3.5rem;
                height: 3.5rem;
                font-size: 2rem;
            }
            
            .main-title {
                font-size: 2rem;
            }
            
            .sub-title {
                font-size: 1rem;
            }
            
            .header-accent {
                display: none;
            }
        }
    </style>
    """, unsafe_allow_html=True)