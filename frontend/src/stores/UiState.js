import {observable, action} from "mobx"

export default class UiState {
    @observable uploadDialogOpen = false;

    constructor(api) {
        this.api = api;
    }

    @action.bound
    openUploadDialog() {
        this.uploadDialogOpen = true;
    }

    @action.bound
    closeUploadDialog() {
        this.uploadDialogOpen = false;
    }
}