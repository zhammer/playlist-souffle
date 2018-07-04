import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { getCurrentPlaylist, getSouffledFrom, getSouffleBy } from 'selectors';
import SouffleStation from './SouffleStation';
import { handleSouffleButtonClicked } from './actions';

const mapStateToProps = (state, props) => ({
  ...props,
  playlist: getCurrentPlaylist(state),
  souffledFrom: getSouffledFrom(state),
  souffleBy: getSouffleBy(state)
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
