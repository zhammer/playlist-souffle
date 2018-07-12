import styled from 'react-emotion';
import colors from 'theme';

const Tile = styled('div')`
  background-color: ${colors.opaqueWhite};
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: .1em;
  margin: .25em;
  height: 3em;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.15rem;
  cursor: pointer;

  @media (min-width: 35em) {
    height: 3.5em;
    margin: .5em;
  }
`;

export default Tile;
