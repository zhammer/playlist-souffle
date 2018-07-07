import React, { Component } from 'react';
import { Spring, animated } from 'react-spring';
import { interpolate } from 'flubber';
import { LinearGradient } from '@vx/gradient';
import colors from 'theme';


const muffinPath = 'M14 3a5 5 0 0 0-4.6-3A5 5 0 0 0 5 3C2.7 3 .9 4.4.2 6.4c-.6 2 .2 4 2 5.2v.3L4 19.3c0 .2.1.3.3.3h10.1c.2 0 .3-.1.3-.3l2-7.2v-.3a4.6 4.6 0 0 0 2-5.3C18 4.4 16.2 3 14 3z';
const notePath = 'M6.9 3v11.2c-.7-.4-1.5-.6-2.4-.6C2 13.6 0 15.1 0 16.8 0 18.6 2 20 4.5 20S9 18.6 9 16.8V6.7l7.9-1.6V12c-.7-.3-1.5-.5-2.4-.5-2.5 0-4.5 1.4-4.5 3.2 0 1.7 2 3.1 4.5 3.1s4.5-1.4 4.5-3.1V.5L6.9 3.1z';
const recordPlayerPath = 'M12.8 14h2.3c.4 0 .8.4.8.7 0 .3-.4.6-.8.6v.4c.6-.3 1.2-.7 1.6-1.3 1.7-2.7-2.4-4.3-2.4-4.3l-2-.8c-2.7-1-10.4 1.2-10.4 1.2-.8.1-1.1-.3-.8-.9L6.8.5c.3-.6 1-.7 1.3 0 0 0 2.5 6.1 5.2 7.2l2 .8s5.4 2 3.1 5.8c-.8 1.4-2 2-3.3 2.2v1.8h.8c.4 0 .7.3.7.6s-.3.6-.7.6H.8c-.5 0-.8-.3-.8-.6s.3-.6.8-.6h.7v-3c-.4 0-.7-.3-.7-.6s.3-.6.7-.6h2.3v-1.2h9V14z';
const whiskPath = 'M17.9.6a2 2 0 0 0-2.9 0L13 2.8a2 2 0 0 0-.3 2.6l-2 2-2.3.8L3.1 10A4.9 4.9 0 0 0 0 14.6c0 2.7 2.1 4.9 4.8 4.9 2 0 3.9-1.4 4.5-3.4l1.7-5 .8-2.6 2-2a2 2 0 0 0 2.4-.2L18.4 4c.4-.4.6-.9.6-1.4 0-.6-.2-1.1-.6-1.5L18 .6z';


class Loading extends Component {
  state = {
    paths: [
      whiskPath,
      notePath,
      recordPlayerPath,
      muffinPath,
    ],
    index: 0
  }
  goNext = () => this.setState(state => ({ index: state.index + 1 >= state.paths.length ? 0 : state.index + 1 }))
  render() {
    const { paths, index } = this.state;
    const interpolator = interpolate(paths[index], paths[index + 1] || paths[0], { maxSegmentLength: 0.1 });
    return (
      <svg width="500" viewBox="0 0 22 22">
        <LinearGradient
          from={colors.lightGreen}
          to={colors.yellow}
          id="gradient" />
        <g fill="url(#gradient)">
          <Spring reset native from={{ t: 0 }} to={{ t: 1 }} onRest={this.goNext}>
            {({ t }) => <animated.path d={t.interpolate(interpolator)} />}
          </Spring>
        </g>
      </svg>
    );
  }
};


export default Loading;
