import styled, { css } from 'react-emotion';
import colors from 'theme';

const base = css`
  color: ${colors.white};
  background: grey;
  font-size: 1.5rem;
  text-transform: uppercase;
  letter-spacing: .1em;
  padding: .5em 3em;
  border-radius: 5em;
  border: solid 0px;
  cursor: pointer;

  @media (min-width: 50em) {
    font-size: 2rem;
  }
`;

const spotify = css`
  background-color: ${colors.green};
  transition: background .05s linear;
  &:hover {
    background: ${colors.lightGreen};
  }
`;

const cta = css`
  color: ${colors.yellow};
`;

export const SpotifyButton = styled('button')(css`${base} ${spotify}`);
export const CtaButton = styled('button')(css`${base} ${cta}`);
