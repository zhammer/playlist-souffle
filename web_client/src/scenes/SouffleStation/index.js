import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { getCurrentPlaylist, getSouffledFrom } from 'selectors';
import SouffleStation from './SouffleStation';
import { handleSouffleButtonClicked } from './actions';

const mapStateToProps = (state, props) => ({
  ...props,
  playlist: getCurrentPlaylist(state),
  souffledFrom: getSouffledFrom(state)
});

const mapDispatchToProps = dispatch => (
  bindActionCreators(
    {
      onSouffleButtonClicked: handleSouffleButtonClicked
    },
    dispatch
  )
);

export default connect(mapStateToProps, mapDispatchToProps)(SouffleStation);
