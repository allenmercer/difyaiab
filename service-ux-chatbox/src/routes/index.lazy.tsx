import { createLazyFileRoute } from '@tanstack/react-router';
import WorkflowCreator from '../components/routes/WorkflowCreatorRoute';

export const Route = createLazyFileRoute('/')({
  component: WorkflowCreator,
});
