export default function Fake500() {
  return (
    <div style={{ 
      backgroundColor: '#fff', 
      color: '#000', 
      minHeight: '100vh', 
      fontFamily: '"Times New Roman", Times, serif',
      padding: '0 8px'
    }}>
      <center>
        <h1 style={{ fontSize: '36px', fontWeight: 'bold', margin: '25px 0 15px 0' }}>
          500 Internal Server Error
        </h1>
      </center>
      <hr style={{ border: 'none', borderTop: '1px solid #ccc', margin: '0' }} />
      <center style={{ fontSize: '14px', margin: '10px 0' }}>
        nginx
      </center>
    </div>
  );
}
