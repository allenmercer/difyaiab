interface DifyEmbedProps {
  src: string;
  title?: string;
}

const DifyEmbed = ({ src, title }: DifyEmbedProps) => {
  return (
    <div style={{ width: '90vw', height: '90vh' }}>
      <iframe
        src={src}
        title={title}
        style={{ border: 'none', width: '100%', height: '100%' }}
      />
    </div>
  );
};

export default DifyEmbed;
