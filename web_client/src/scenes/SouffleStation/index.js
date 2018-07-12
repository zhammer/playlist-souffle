import { connect } from 'react-redux';
import { getCurrentPlaylist, getSouffledFrom, getSouffleBy } from 'selectors';
import SouffleStation from './SouffleStation';
import { handleSouffleButtonClicked, handleBackButtonClicked, handleToggleButtonClicked } from './actions';

const mapStateToProps = (state, props) => ({
  ...props,
  playlist: getCurrentPlaylist(state),
  souffledFrom: getSouffledFrom(state),
  souffleBy: getSouffleBy(state)
});

const mapDispatchToProps = {
  onSouffleButtonClicked: handleSouffleButtonClicked,
  onBackButtonClicked: handleBackButtonClicked,
  onToggleButtonClicked: handleToggleButtonClicked
};

export default connect(mapStateToProps, mapDispatchToProps)(SouffleStation);
