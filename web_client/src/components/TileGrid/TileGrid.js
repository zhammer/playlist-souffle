import styled from 'react-emotion';

/**
 *  A responsive Tile grid.
 */
const TileGrid = styled('div')`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(20em, 1fr));
  grid-auto-rows: 1fr;
`;

export default TileGrid;
