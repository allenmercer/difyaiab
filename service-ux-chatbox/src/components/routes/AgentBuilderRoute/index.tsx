import DifyEmbed from '../../dify-iframe/DifyEmbed';

const AgentBuilder = () => {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
      }}>
      <DifyEmbed src={import.meta.env.VITE_DIFY_EMBED} title='Dify Studio' />
    </div>
  );
};

export default AgentBuilder;
