import styled from 'react-emotion';
import colors from 'theme';
import SouffleHeroGif from './SouffleHero.gif';

const SouffleHero = styled('div')`
  background: white;
  margin-top: 1em;
  height: 12em;
  background-image: url(${SouffleHeroGif});
  background-color: ${colors.yellow};
  background-size: cover;
  background-position: center;
  background-blend-mode: luminosity;

  @media (min-width: 35em) {
    margin-top: 2em;
    background-size: 35em;
    height: 20em;
  }

  @media (min-width: 50em) {
    background-size: 50em;
  }
`;


export default SouffleHero;
