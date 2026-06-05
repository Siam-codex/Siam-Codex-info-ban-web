# app.py - Complete website with FULL information display
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Info Hub | Professional Ban Check</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #000000;
            color: #ffffff;
            overflow-x: hidden;
        }
        
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: radial-gradient(circle at 20% 30%, #1a1a1a 0%, #000000 100%);
        }
        
        .bg-animation::before {
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            top: -50%;
            left: -50%;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 50px,
                rgba(255,255,255,0.02) 50px,
                rgba(255,255,255,0.02) 100px
            );
            animation: moveBg 20s linear infinite;
        }
        
        @keyframes moveBg {
            0% { transform: translate(0, 0); }
            100% { transform: translate(100px, 100px); }
        }
        
        .loading {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.95);
            backdrop-filter: blur(10px);
            z-index: 1000;
            display: none;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        
        .loading.active { display: flex; }
        
        .spinner {
            width: 60px;
            height: 60px;
            border: 3px solid rgba(255,255,255,0.1);
            border-top: 3px solid #ffffff;
            border-radius: 50%;
            animation: spin 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            margin-top: 20px;
            font-size: 14px;
            letter-spacing: 3px;
            font-weight: 500;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .hero {
            text-align: center;
            padding: 3rem 1rem 4rem;
            animation: slideDown 0.8s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .hero h1 {
            font-size: 4rem;
            font-weight: 800;
            letter-spacing: 10px;
            background: linear-gradient(135deg, #ffffff 0%, #888888 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 3s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.3); }
        }
        
        .hero p {
            color: rgba(255,255,255,0.6);
            letter-spacing: 2px;
            margin-top: 1rem;
        }
        
        .hero-line {
            width: 100px;
            height: 2px;
            background: linear-gradient(90deg, transparent, #ffffff, transparent);
            margin: 1.5rem auto 0;
        }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 2rem 0;
        }
        
        @media (max-width: 900px) {
            .grid { grid-template-columns: 1fr; }
            .hero h1 { font-size: 2rem; letter-spacing: 5px; }
        }
        
        .card {
            background: rgba(10,10,10,0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 2rem;
            transition: all 0.3s ease;
            animation: fadeUp 0.6s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            border-color: rgba(255,255,255,0.3);
            box-shadow: 0 10px 40px rgba(255,255,255,0.05);
        }
        
        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .card-icon {
            width: 50px;
            height: 50px;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .card-header h2 {
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        .badge {
            font-size: 0.7rem;
            padding: 0.2rem 0.6rem;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            margin-left: 10px;
        }
        
        .badge.pro {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .card-desc {
            color: rgba(255,255,255,0.5);
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }
        
        .input-group {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        @media (max-width: 600px) {
            .input-group { flex-direction: column; }
        }
        
        input {
            flex: 1;
            background: rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 0.9rem 1.2rem;
            border-radius: 12px;
            color: white;
            font-size: 0.95rem;
            transition: all 0.3s;
        }
        
        input:focus {
            outline: none;
            border-color: white;
            background: black;
        }
        
        input::placeholder {
            color: rgba(255,255,255,0.3);
        }
        
        button {
            padding: 0.9rem 2rem;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-family: inherit;
        }
        
        .btn-primary {
            background: white;
            color: black;
        }
        
        .btn-primary:hover {
            background: rgba(255,255,255,0.9);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(255,255,255,0.2);
        }
        
        .btn-secondary {
            background: transparent;
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .btn-secondary:hover {
            background: rgba(255,255,255,0.05);
            border-color: white;
            transform: translateY(-2px);
        }
        
        .result {
            margin-top: 1.5rem;
            padding: 1rem;
            background: rgba(0,0,0,0.5);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            display: none;
            animation: fadeIn 0.5s;
            max-height: 600px;
            overflow-y: auto;
        }
        
        .result.active { display: block; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .result-row {
            display: flex;
            justify-content: space-between;
            padding: 0.8rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .result-label {
            color: rgba(255,255,255,0.5);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 1px;
            min-width: 150px;
        }
        
        .result-value {
            font-weight: 500;
            word-break: break-all;
            flex: 1;
            text-align: right;
        }
        
        .status-banned { color: #ff4444; font-weight: bold; }
        .status-clean { color: #44ff44; font-weight: bold; }
        
        .error-message {
            color: #ff4444;
            text-align: center;
            padding: 1rem;
        }
        
        .info-section {
            margin-bottom: 1.5rem;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 1rem;
        }
        
        .info-title {
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 1px;
            color: #ffffff;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .array-values {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: flex-end;
        }
        
        .array-tag {
            background: rgba(255,255,255,0.1);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            margin-top: 2rem;
            border-top: 1px solid rgba(255,255,255,0.05);
            color: rgba(255,255,255,0.3);
            font-size: 0.8rem;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #000000;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #333333;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div id="loading" class="loading">
        <div class="spinner"></div>
        <div class="loading-text">FETCHING DATA</div>
    </div>
    
    <div class="container">
        <div class="hero">
            <h1>GAMEINFO HUB</h1>
            <p>PROFESSIONAL GAMING INTELLIGENCE PLATFORM</p>
            <div class="hero-line"></div>
        </div>
       <div style="text-align: center; margin: -10px 0 20px 0;">
    <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #FFD700; font-weight: bold; font-family: monospace; font-size: 18px; letter-spacing: 3px;">
        👑 🔥 MAKE BY SIAM CODEX 🔥👑 
    </marquee>
</div>
        
        <div class="grid">
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🔍</div>
                    <h2>Ban Status Checker <span class="badge">REAL-TIME</span></h2>
                </div>
                <p class="card-desc">Check if any game account has been banned or restricted</p>
                <div class="input-group">
                    <input type="text" id="banUid" placeholder="Enter UID (e.g., 1234567890)">
                    <button class="btn-primary" id="checkBan">CHECK BAN</button>
                </div>
                <div id="banResult" class="result"></div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">📊</div>
                    <h2>Complete Account Info <span class="badge pro">PRO</span></h2>
                </div>
                <p class="card-desc">Get detailed statistics, clan info, social data & more</p>
                <div class="input-group">
                    <input type="text" id="infoUid" placeholder="Enter UID for full details">
                    <button class="btn-secondary" id="checkInfo">FETCH INFO</button>
                </div>
                <div id="infoResult" class="result"></div>
            </div>
        </div>
        
        <footer>
            <p>© 2026 GameInfo Hub — Powered by SIAM CODEX Gaming Intelligence API</p>
        </footer>
    </div>
    
    <script>
        const loading = document.getElementById('loading');
        
        function showLoading() { loading.classList.add('active'); }
        function hideLoading() { setTimeout(() => loading.classList.remove('active'), 300); }
        
        function escapeHtml(str) {
            if (!str && str !== 0) return 'N/A';
            return String(str).replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }
        
        function formatArray(arr) {
            if (!arr || !Array.isArray(arr)) return 'N/A';
            if (arr.length === 0) return 'Empty';
            return `<div class="array-values">${arr.map(v => `<span class="array-tag">${escapeHtml(v)}</span>`).join('')}</div>`;
        }
        
        function formatObject(obj, indent = 0) {
            if (!obj) return 'N/A';
            let html = '<div style="margin-left: ' + (indent * 20) + 'px">';
            for (let [key, value] of Object.entries(obj)) {
                html += `<div class="result-row">
                            <span class="result-label">${escapeHtml(key.toUpperCase())}</span>
                            <span class="result-value">${typeof value === 'object' ? formatObject(value, indent + 1) : escapeHtml(value)}</span>
                         </div>`;
            }
            html += '</div>';
            return html;
        }
        
        async function callApi(url, uid, resultDiv, isBanCheck) {
            if (!uid || uid.trim() === '') {
                resultDiv.innerHTML = '<div class="error-message">⚠️ Please enter a valid UID</div>';
                resultDiv.classList.add('active');
                return;
            }
            
            showLoading();
            resultDiv.classList.remove('active');
            
            try {
                const response = await fetch(`${url}?uid=${encodeURIComponent(uid.trim())}`);
                const data = await response.json();
                
                setTimeout(() => {
                    if (isBanCheck) {
                        if (data.error) {
                            resultDiv.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
                        } else {
                            const isBanned = data.ban_status !== 'Not banned';
                            resultDiv.innerHTML = `
                                <div class="result-row"><span class="result-label">PLAYER NAME</span><span class="result-value">${escapeHtml(data.name)}</span></div>
                                <div class="result-row"><span class="result-label">REGION</span><span class="result-value">${escapeHtml(data.region)}</span></div>
                                <div class="result-row"><span class="result-label">BAN STATUS</span><span class="result-value ${isBanned ? 'status-banned' : 'status-clean'}">${isBanned ? '🔴 BANNED' : '🟢 NOT BANNED'}</span></div>
                                ${data.ban_since ? `<div class="result-row"><span class="result-label">BAN SINCE</span><span class="result-value status-banned">⚠️ ${escapeHtml(data.ban_since)}</span></div>` : ''}
                            `;
                        }
                    } else {
                        if (data.error) {
                            resultDiv.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
                        } else {
                            let html = '';
                            
                            // BASIC INFO - Full Details
                            if (data.basic_info) {
                                html += `<div class="info-section">
                                    <div class="info-title">📋 BASIC INFORMATION</div>
                                    <div class="result-row"><span class="result-label">Account ID</span><span class="result-value">${escapeHtml(data.basic_info.account_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Account Type</span><span class="result-value">${escapeHtml(data.basic_info.account_type)}</span></div>
                                    <div class="result-row"><span class="result-label">Nickname</span><span class="result-value">${escapeHtml(data.basic_info.nickname)}</span></div>
                                    <div class="result-row"><span class="result-label">Region</span><span class="result-value">${escapeHtml(data.basic_info.region)}</span></div>
                                    <div class="result-row"><span class="result-label">Level</span><span class="result-value">${escapeHtml(data.basic_info.level)}</span></div>
                                    <div class="result-row"><span class="result-label">Experience (XP)</span><span class="result-value">${escapeHtml(data.basic_info.exp)}</span></div>
                                    <div class="result-row"><span class="result-label">Banner ID</span><span class="result-value">${escapeHtml(data.basic_info.banner_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Head Pic</span><span class="result-value">${escapeHtml(data.basic_info.head_pic)}</span></div>
                                    <div class="result-row"><span class="result-label">Rank</span><span class="result-value">${escapeHtml(data.basic_info.rank)}</span></div>
                                    <div class="result-row"><span class="result-label">Ranking Points</span><span class="result-value">${escapeHtml(data.basic_info.ranking_points)}</span></div>
                                    <div class="result-row"><span class="result-label">Has Elite Pass</span><span class="result-value">${data.basic_info.has_elite_pass ? '✅ Yes' : '❌ No'}</span></div>
                                    <div class="result-row"><span class="result-label">Badge Count</span><span class="result-value">${escapeHtml(data.basic_info.badge_cnt)}</span></div>
                                    <div class="result-row"><span class="result-label">Badge ID</span><span class="result-value">${escapeHtml(data.basic_info.badge_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Season ID</span><span class="result-value">${escapeHtml(data.basic_info.season_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Liked Count</span><span class="result-value">❤️ ${escapeHtml(data.basic_info.liked)}</span></div>
                                    <div class="result-row"><span class="result-label">Show Rank</span><span class="result-value">${data.basic_info.show_rank ? '✅ Yes' : '❌ No'}</span></div>
                                    <div class="result-row"><span class="result-label">Last Login</span><span class="result-value">${escapeHtml(data.basic_info.last_login_at)}</span></div>
                                    <div class="result-row"><span class="result-label">CS Rank</span><span class="result-value">${escapeHtml(data.basic_info.cs_rank)}</span></div>
                                    <div class="result-row"><span class="result-label">CS Ranking Points</span><span class="result-value">${escapeHtml(data.basic_info.cs_ranking_points)}</span></div>
                                    <div class="result-row"><span class="result-label">Weapon Skins</span><span class="result-value">${formatArray(data.basic_info.weapon_skin_shows)}</span></div>
                                    <div class="result-row"><span class="result-label">Pin ID</span><span class="result-value">${escapeHtml(data.basic_info.pin_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Max Rank</span><span class="result-value">${escapeHtml(data.basic_info.max_rank)}</span></div>
                                    <div class="result-row"><span class="result-label">CS Max Rank</span><span class="result-value">${escapeHtml(data.basic_info.cs_max_rank)}</span></div>
                                    <div class="result-row"><span class="result-label">Game Bag Show</span><span class="result-value">${escapeHtml(data.basic_info.game_bag_show)}</span></div>
                                    <div class="result-row"><span class="result-label">Clan ID</span><span class="result-value">${escapeHtml(data.basic_info.clan_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Hide Personal Info</span><span class="result-value">${data.basic_info.account_prefers?.hide_personal_info ? '✅ Yes' : '❌ No'}</span></div>
                                    <div class="result-row"><span class="result-label">Prime Level</span><span class="result-value">${escapeHtml(data.basic_info.prime_info?.prime_level)}</span></div>
                                </div>`;
                            }
                            
                            // PROFILE INFO
                            if (data.profile_info) {
                                html += `<div class="info-section">
                                    <div class="info-title">👤 PROFILE INFORMATION</div>
                                    <div class="result-row"><span class="result-label">Avatar ID</span><span class="result-value">${escapeHtml(data.profile_info.avatar_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Skin Color</span><span class="result-value">${escapeHtml(data.profile_info.skin_color)}</span></div>
                                    <div class="result-row"><span class="result-label">Clothes</span><span class="result-value">${formatArray(data.profile_info.clothes)}</span></div>
                                    <div class="result-row"><span class="result-label">Equipped Skills</span><span class="result-value">${formatArray(data.profile_info.equiped_skills)}</span></div>
                                    <div class="result-row"><span class="result-label">Is Selected</span><span class="result-value">${data.profile_info.is_selected ? '✅ Yes' : '❌ No'}</span></div>
                                    <div class="result-row"><span class="result-label">Is Selected Awaken</span><span class="result-value">${data.profile_info.is_selected_awaken ? '✅ Yes' : '❌ No'}</span></div>
                                </div>`;
                            }
                            
                            // CLAN INFO
                            if (data.clan_basic_info && data.clan_basic_info.clan_name) {
                                html += `<div class="info-section">
                                    <div class="info-title">🏆 CLAN INFORMATION</div>
                                    <div class="result-row"><span class="result-label">Clan ID</span><span class="result-value">${escapeHtml(data.clan_basic_info.clan_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Clan Name</span><span class="result-value">${escapeHtml(data.clan_basic_info.clan_name)}</span></div>
                                    <div class="result-row"><span class="result-label">Captain ID</span><span class="result-value">${escapeHtml(data.clan_basic_info.captain_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Clan Level</span><span class="result-value">${escapeHtml(data.clan_basic_info.clan_level)}</span></div>
                                    <div class="result-row"><span class="result-label">Capacity</span><span class="result-value">${escapeHtml(data.clan_basic_info.capacity)}</span></div>
                                    <div class="result-row"><span class="result-label">Member Count</span><span class="result-value">${escapeHtml(data.clan_basic_info.member_num)}</span></div>
                                </div>`;
                            }
                            
                            // CAPTAIN INFO
                            if (data.captain_basic_info) {
                                html += `<div class="info-section">
                                    <div class="info-title">👑 CAPTAIN INFORMATION</div>
                                    <div class="result-row"><span class="result-label">Captain Name</span><span class="result-value">${escapeHtml(data.captain_basic_info.nickname)}</span></div>
                                    <div class="result-row"><span class="result-label">Captain Level</span><span class="result-value">${escapeHtml(data.captain_basic_info.level)}</span></div>
                                    <div class="result-row"><span class="result-label">Captain Rank</span><span class="result-value">${escapeHtml(data.captain_basic_info.rank)}</span></div>
                                </div>`;
                            }
                            
                            // PET INFO
                            if (data.pet_info) {
                                html += `<div class="info-section">
                                    <div class="info-title">🐾 PET INFORMATION</div>
                                    <div class="result-row"><span class="result-label">Pet ID</span><span class="result-value">${escapeHtml(data.pet_info.id)}</span></div>
                                    <div class="result-row"><span class="result-label">Pet Name</span><span class="result-value">${escapeHtml(data.pet_info.name)}</span></div>
                                    <div class="result-row"><span class="result-label">Pet Level</span><span class="result-value">${escapeHtml(data.pet_info.level)}</span></div>
                                    <div class="result-row"><span class="result-label">Pet XP</span><span class="result-value">${escapeHtml(data.pet_info.exp)}</span></div>
                                    <div class="result-row"><span class="result-label">Is Selected</span><span class="result-value">${data.pet_info.is_selected ? '✅ Yes' : '❌ No'}</span></div>
                                    <div class="result-row"><span class="result-label">Skin ID</span><span class="result-value">${escapeHtml(data.pet_info.skin_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Selected Skill ID</span><span class="result-value">${escapeHtml(data.pet_info.selected_skill_id)}</span></div>
                                </div>`;
                            }
                            
                            // SOCIAL INFO
                            if (data.social_info) {
                                html += `<div class="info-section">
                                    <div class="info-title">💬 SOCIAL INFORMATION</div>
                                    <div class="result-row"><span class="result-label">Account ID</span><span class="result-value">${escapeHtml(data.social_info.account_id)}</span></div>
                                    <div class="result-row"><span class="result-label">Gender</span><span class="result-value">${escapeHtml(data.social_info.gender)}</span></div>
                                    <div class="result-row"><span class="result-label">Language</span><span class="result-value">${escapeHtml(data.social_info.language)}</span></div>
                                    <div class="result-row"><span class="result-label">Mode Prefer</span><span class="result-value">${escapeHtml(data.social_info.mode_prefer)}</span></div>
                                    <div class="result-row"><span class="result-label">Signature</span><span class="result-value">${escapeHtml(data.social_info.signature) || 'No signature'}</span></div>
                                    <div class="result-row"><span class="result-label">Rank Show</span><span class="result-value">${escapeHtml(data.social_info.rank_show)}</span></div>
                                </div>`;
                            }
                            
                            // DIAMOND COST
                            if (data.diamond_cost_res) {
                                html += `<div class="info-section">
                                    <div class="info-title">💎 DIAMOND INFORMATION</div>
                                    <div class="result-row"><span class="result-label">Diamond Cost</span><span class="result-value">💎 ${escapeHtml(data.diamond_cost_res.diamond_cost)}</span></div>
                                </div>`;
                            }
                            
                            // CREDIT SCORE
                            if (data.credit_score_info) {
                                html += `<div class="info-section">
                                    <div class="info-title">⭐ CREDIT SCORE</div>
                                    <div class="result-row"><span class="result-label">Credit Score</span><span class="result-value">${escapeHtml(data.credit_score_info.credit_score)}/100</span></div>
                                    <div class="result-row"><span class="result-label">Reward State</span><span class="result-value">${escapeHtml(data.credit_score_info.reward_state)}</span></div>
                                    <div class="result-row"><span class="result-label">Periodic Summary End</span><span class="result-value">${escapeHtml(data.credit_score_info.periodic_summary_end_time)}</span></div>
                                </div>`;
                            }
                            
                            resultDiv.innerHTML = html;
                        }
                    }
                    resultDiv.classList.add('active');
                    hideLoading();
                }, 500);
                
            } catch(error) {
                setTimeout(() => {
                    resultDiv.innerHTML = `<div class="error-message">❌ Network Error: ${error.message}</div>`;
                    resultDiv.classList.add('active');
                    hideLoading();
                }, 500);
            }
        }
        
        document.getElementById('checkBan').onclick = () => {
            const uid = document.getElementById('banUid').value;
            callApi('/api/bancheck', uid, document.getElementById('banResult'), true);
        };
        
        document.getElementById('checkInfo').onclick = () => {
            const uid = document.getElementById('infoUid').value;
            callApi('/api/fullinfo', uid, document.getElementById('infoResult'), false);
        };
        
        document.getElementById('banUid').onkeypress = (e) => {
            if (e.key === 'Enter') document.getElementById('checkBan').click();
        };
        
        document.getElementById('infoUid').onkeypress = (e) => {
            if (e.key === 'Enter') document.getElementById('checkInfo').click();
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/bancheck')
def ban_check():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({'error': 'UID required'}), 400
    
    try:
        resp = requests.get(f'https://ban-check-api-lilac.vercel.app/bancheck?uid={uid}', timeout=10)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fullinfo')
def full_info():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({'error': 'UID required'}), 400
    
    try:
        resp = requests.get(f'https://star-info-api.lovable.app/functions/v1/info-api/accinfo?uid={uid}', timeout=15)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SIAM CODEX SERVER STARTED SUCCESSFULLY!")
    print("📱 Open browser: http://localhost:5000")
    print("⚡ Press CTRL+C to stop")
    print("👨‍💻\033[94m  DEVELOPED BY 🔥👑🗿SIAM CODEX🗿👑🔥\033[0m")
    print("="*60 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000)
