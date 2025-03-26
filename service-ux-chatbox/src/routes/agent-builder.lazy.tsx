import { createLazyFileRoute } from '@tanstack/react-router';
import AgentBuilder from '../components/routes/AgentBuilderRoute';

export const Route = createLazyFileRoute('/agent-builder')({
  component: AgentBuilder,
});
