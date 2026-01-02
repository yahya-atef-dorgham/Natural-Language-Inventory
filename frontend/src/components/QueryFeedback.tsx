import React from 'react';

export interface QueryFeedbackProps {
  message?: string;
  reviewSummary?: Record<string, unknown>;
  status?: string;
}

export const QueryFeedback: React.FC<QueryFeedbackProps> = ({
  message,
  reviewSummary,
  status,
}) => {
  if (!message && !reviewSummary) {
    return null;
  }

  const isError = status === 'rejected' || status === 'failed';
  const isWarning = status === 'reviewing' || (reviewSummary && Object.keys(reviewSummary).length > 0);

  return (
    <div className={`query-feedback ${isError ? 'error' : isWarning ? 'warning' : 'info'}`}>
      {message && <p className="message">{message}</p>}
      {reviewSummary && Object.keys(reviewSummary).length > 0 && (
        <div className="review-summary">
          <h4>Query Review Summary</h4>
          <pre>{JSON.stringify(reviewSummary, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

