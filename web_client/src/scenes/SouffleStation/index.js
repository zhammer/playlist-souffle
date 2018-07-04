import { connect } from 'react-redux';
import { getCurrentPlaylist } from 'selectors';
import SouffleStation from './SouffleStation';

const mapStateToProps = (state, props) => ({
  ...props,
  playlist: getCurrentPlaylist(state)
});

export default connect(mapStateToProps)(SouffleStation);
