<div class="cover-page">
<style>
.cover-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    max-width: 71vh;
    margin: 0 auto;
    background: linear-gradient(135deg, #5b6abf 0%, #6c5ce7 30%, #8b5cf6 60%, #7c3aed 100%);
    padding: 40px;
    position: relative;
    overflow: hidden;
}
.cover-page::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 30px 30px;
    pointer-events: none;
}
.cover-page .orb { position: absolute; border-radius: 50%; pointer-events: none; }
.cover-page .orb-1 { width: 300px; height: 300px; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); top: -60px; right: -80px; }
.cover-page .orb-2 { width: 200px; height: 200px; background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%); bottom: 40px; left: -50px; }
.cover-page .network-container { position: relative; width: 180px; height: 180px; margin-bottom: 30px; z-index: 1; }
.cover-page .network-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
.cover-page .mnode { position: absolute; border-radius: 50%; z-index: 2; }
.cover-page .mnode.agent { width: 16px; height: 16px; background: #fff; box-shadow: 0 0 18px rgba(255,255,255,0.7), 0 0 40px rgba(255,255,255,0.25); top: 78px; left: 78px; }
.cover-page .mnode.working { width: 9px; height: 9px; background: rgba(255,220,180,0.9); box-shadow: 0 0 10px rgba(255,220,180,0.5); }
.cover-page .w1 { top: 65px; left: 90px; }
.cover-page .w2 { top: 76px; left: 62px; }
.cover-page .w3 { top: 67px; left: 70px; }
.cover-page .mnode.short { width: 11px; height: 11px; background: rgba(180,160,255,0.85); box-shadow: 0 0 12px rgba(180,160,255,0.5); }
.cover-page .s1 { top: 45px; left: 80px; }
.cover-page .s2 { top: 83px; left: 42px; }
.cover-page .s3 { top: 53px; left: 112px; }
.cover-page .s4 { top: 95px; left: 117px; }
.cover-page .mnode.long { width: 13px; height: 13px; background: rgba(130,120,255,0.7); box-shadow: 0 0 14px rgba(130,120,255,0.4); }
.cover-page .l1 { top: 25px; left: 89px; }
.cover-page .l2 { top: 98px; left: 28px; }
.cover-page .l3 { top: 33px; left: 20px; }
.cover-page .l4 { top: 111px; left: 67px; }
.cover-page .l5 { top: 28px; left: 123px; }
.cover-page .l6 { top: 123px; left: 112px; }
.cover-page .mnode.reflect { width: 12px; height: 12px; background: rgba(255,200,120,0.9); box-shadow: 0 0 14px rgba(255,200,120,0.5); top: 47px; left: 50px; }
.cover-page .title-area { z-index: 1; text-align: center; }
.cover-page .title-cn { font-size: 42px; font-weight: 700; color: #fff; letter-spacing: 6px; line-height: 1.35; text-shadow: 0 2px 20px rgba(0,0,0,0.15); }
.cover-page .title-cn strong { font-weight: 800; }
.cover-page .title-divider { width: 60px; height: 2px; background: rgba(255,255,255,0.5); margin: 20px auto; border-radius: 1px; }
.cover-page .title-en { font-size: 14px; color: rgba(255,255,255,0.65); letter-spacing: 4px; text-transform: uppercase; font-weight: 400; }
.cover-page .author-area { z-index: 1; text-align: center; margin-top: 40px; }
.cover-page .author-name { font-size: 16px; color: rgba(255,255,255,0.85); letter-spacing: 2px; font-weight: 500; }
.cover-page .author-sub { font-size: 12px; color: rgba(255,255,255,0.4); letter-spacing: 1px; margin-top: 8px; }
</style>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<div class="network-container">
    <svg class="network-svg" viewBox="0 0 160 160">
        <line x1="86" y1="86" x2="94" y2="69" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
        <line x1="86" y1="86" x2="66" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
        <line x1="86" y1="86" x2="74" y2="71" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
        <line x1="86" y1="86" x2="86" y2="50" stroke="rgba(180,160,255,0.3)" stroke-width="1"/>
        <line x1="86" y1="86" x2="48" y2="89" stroke="rgba(180,160,255,0.3)" stroke-width="1"/>
        <line x1="86" y1="86" x2="118" y2="59" stroke="rgba(180,160,255,0.3)" stroke-width="1"/>
        <line x1="86" y1="86" x2="123" y2="101" stroke="rgba(180,160,255,0.3)" stroke-width="1"/>
        <line x1="86" y1="86" x2="96" y2="31" stroke="rgba(130,120,255,0.25)" stroke-width="1"/>
        <line x1="86" y1="86" x2="35" y2="105" stroke="rgba(130,120,255,0.25)" stroke-width="1"/>
        <line x1="86" y1="86" x2="27" y2="40" stroke="rgba(130,120,255,0.25)" stroke-width="1"/>
        <line x1="86" y1="86" x2="74" y2="118" stroke="rgba(130,120,255,0.25)" stroke-width="1"/>
        <line x1="86" y1="86" x2="130" y2="35" stroke="rgba(130,120,255,0.25)" stroke-width="1"/>
        <line x1="86" y1="86" x2="119" y2="130" stroke="rgba(130,120,255,0.25)" stroke-width="1"/>
        <line x1="86" y1="86" x2="56" y2="54" stroke="rgba(255,200,120,0.35)" stroke-width="1.5"/>
        <line x1="94" y1="69" x2="86" y2="50" stroke="rgba(255,255,255,0.12)" stroke-width="0.8"/>
        <line x1="86" y1="50" x2="96" y2="31" stroke="rgba(255,255,255,0.1)" stroke-width="0.8"/>
        <line x1="96" y1="31" x2="118" y2="59" stroke="rgba(255,255,255,0.1)" stroke-width="0.8"/>
        <line x1="118" y1="59" x2="123" y2="101" stroke="rgba(255,255,255,0.1)" stroke-width="0.8"/>
        <line x1="123" y2="101" x2="74" y2="118" stroke="rgba(255,255,255,0.1)" stroke-width="0.8"/>
        <line x1="74" y2="118" x2="35" y2="105" stroke="rgba(255,255,255,0.1)" stroke-width="0.8"/>
        <line x1="35" y2="105" x2="27" y2="40" stroke="rgba(255,255,255,0.1)" stroke-width="0.8"/>
        <line x1="27" y2="40" x2="86" y2="50" stroke="rgba(255,255,255,0.1)" stroke-width="0.8"/>
        <line x1="56" y1="54" x2="86" y2="50" stroke="rgba(255,200,120,0.15)" stroke-width="0.8"/>
        <line x1="56" y1="54" x2="48" y2="89" stroke="rgba(255,200,120,0.15)" stroke-width="0.8"/>
    </svg>
    <div class="mnode agent"></div>
    <div class="mnode working w1"></div>
    <div class="mnode working w2"></div>
    <div class="mnode working w3"></div>
    <div class="mnode short s1"></div>
    <div class="mnode short s2"></div>
    <div class="mnode short s3"></div>
    <div class="mnode short s4"></div>
    <div class="mnode long l1"></div>
    <div class="mnode long l2"></div>
    <div class="mnode long l3"></div>
    <div class="mnode long l4"></div>
    <div class="mnode long l5"></div>
    <div class="mnode long l6"></div>
    <div class="mnode reflect"></div>
</div>

<div class="title-area">
    <div class="title-cn">智能体<br><strong>记忆工程</strong></div>
    <div class="title-divider"></div>
    <div class="title-en">Agent Memory Engineering</div>
</div>

<div class="author-area">
    <div class="author-name">xPaperReader &amp; Ocean</div>
    <div class="author-sub">v1.0.0 · 2026</div>
</div>
</div>
