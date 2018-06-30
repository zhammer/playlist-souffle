import React from 'react';
import queryString from 'query-string';

const connectRouter = mapRouterQueryParamsToProps => WrappedComponent => (
  props => {
    const { location: { search }, ...rest } = props;
    const queryStringParams = queryString.parse(search);
    const queryStringProps = mapRouterQueryParamsToProps(queryStringParams);

    return <WrappedComponent { ...rest } { ...queryStringProps }/>;
  }
);

export default connectRouter;
