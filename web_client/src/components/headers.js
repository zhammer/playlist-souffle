import styled, { css } from 'react-emotion';
import colors from 'theme';

const h1Css = css`
  font-family: 'Monoton', cursive;
  font-size: 2.5rem;
  text-align: center;
  color: ${colors.yellow};
  letter-spacing: .09em;
  line-height: 1em;
  margin-left: 1.5em;
  margin-right: 1.5em;
  margin-top: .75em;
  margin-bottom: .5em;

  @media (min-width: 35em) {
    margin-bottom: .75em;
    margin-top: 1em;
    font-size: 3rem;
  }
`;

const h3h4Base = css`
  color: ${colors.white};
  text-align: center;
  letter-spacing: .03em;
  margin-left: 1.5em;
  margin-right: 1.5em;
  line-height: 1.25em;
  margin-top: 0;
  margin-bottom: .5em;
`;

const h3Css = css`
  font-size: 1.25rem;
  @media (min-width: 35em) {
    font-size: 1.75rem;
  }
`;

const h4Css = css`
  font-size: 1rem;
  @media (min-width: 35em) {
    font-size: 1.5rem;
  }
`;

const StyledH1 = styled('h1')(h1Css);
const StyledH3 = styled('h3')(css`${h3h4Base} ${h3Css}`);
const StyledH4 = styled('h4')(css`${h3h4Base} ${h4Css}`);

export { StyledH1, StyledH3, StyledH4 };
