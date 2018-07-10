import styled from 'react-emotion';

/**
 *  A column of children.
 */
const TileColumn = styled('div')`
  display: grid;
  grid-template-columns: 1fr;
  grid-auto-rows: 1fr;
`;

export default TileColumn;
