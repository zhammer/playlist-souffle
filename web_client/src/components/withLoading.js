import React from 'react';

/**
 *  HOC that returns a component which renders `WrappedComponent` if its `loading` prop is false and
 *  renders `LoadingComponent` if its `loading` true is false.
 */
const withLoading = (WrappedComponent, LoadingComponent) => ({ loading, ...props }) => (
  loading ? <LoadingComponent /> : <WrappedComponent { ...props } />
);

export default withLoading;
