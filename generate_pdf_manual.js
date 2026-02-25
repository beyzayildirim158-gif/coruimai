// Manual PDF Generator Script
const { Pool } = require('pg');

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'instagram_ai',
  user: 'admin',
  password: 'password'
});

async function generatePDF(analysisId) {
  const client = await pool.connect();
  
  try {
    // Get analysis data
    const analysisResult = await client.query(`
      SELECT 
        a.id,
        a.agent_results,
        a.overall_score,
        a.score_grade,
        a.recommendations,
        ia.username,
        ia.followers,
        ia.following,
        ia.posts,
        ia.engagement_rate,
        ia.bio,
        ia.profile_pic_url,
        ia.avg_likes,
        ia.avg_comments,
        ia.is_verified,
        ia.is_business,
        ia.bot_score
      FROM analyses a
      JOIN instagram_accounts ia ON a.account_id = ia.id
      WHERE a.id = $1
    `, [analysisId]);
    
    if (analysisResult.rows.length === 0) {
      throw new Error('Analysis not found');
    }
    
    const data = analysisResult.rows[0];
    const agentResults = data.agent_results || {};
    
    // Build payload
    const payload = {
      reportId: `report-${Date.now()}`,
      analysisId: analysisId,
      accountData: {
        username: data.username,
        followers: data.followers,
        following: data.following,
        posts: data.posts,
        engagementRate: parseFloat(data.engagement_rate) || 0,
        bio: data.bio,
        profilePicUrl: data.profile_pic_url,
        avgLikes: parseFloat(data.avg_likes) || 0,
        avgComments: parseFloat(data.avg_comments) || 0,
        verified: data.is_verified,
        isBusiness: data.is_business,
        botScore: parseFloat(data.bot_score) || 0
      },
      agentResults: agentResults,
      eli5Report: agentResults.eli5Report || null,
      finalVerdict: agentResults.finalVerdict || null,
      businessIdentity: agentResults.businessIdentity || null,
      advancedAnalysis: agentResults.advancedAnalysis || null,
      sanitizationReport: agentResults.sanitizationReport || null,
      hardValidation: agentResults.hardValidation || null,
      overallScore: parseFloat(data.overall_score) || null,
      scoreGrade: data.score_grade || null,
      recommendations: data.recommendations || [],
      tier: 'PRO'
    };
    
    console.log('Sending payload to PDF generator...');
    console.log('Account:', payload.accountData.username);
    console.log('Score:', payload.overallScore, payload.scoreGrade);
    console.log('Has advancedAnalysis:', !!payload.advancedAnalysis);
    console.log('Has eli5Report:', !!payload.eli5Report);
    
    // Send to PDF generator
    const response = await fetch('http://localhost:3002/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    const result = await response.json();
    console.log('\nPDF Generated:');
    console.log(JSON.stringify(result, null, 2));
    
    return result;
    
  } finally {
    client.release();
    await pool.end();
  }
}

const analysisId = process.argv[2] || '07113fcf-aa84-4b25-852e-5ceab49b4977';
generatePDF(analysisId).catch(console.error);
