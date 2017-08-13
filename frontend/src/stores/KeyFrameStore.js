import {observable, action} from "mobx"

export default class KeyFrameStore {
    api;
    @observable keyFrames = [];
    @observable labeledPredictions = [];
    @observable currentPage = 0;
    @observable totalPages = 1;
    lastQuery;

    constructor(api) {
        this.api = api;
    }

    @action.bound
    async loadKeyFrames(query, page = 0) {

        this.lastQuery = query;

        if (query) {
            const res = await this.api.get('/api/search', {
                body: {
                    q: query,
                    page: page
                }
            });

            if (res.ok) {
                this.keyFrames = res.body.key_frames;
                this.labeledPredictions = res.body.labeled_predictions;
                this.totalPages = res.body.total_pages;
                this.currentPage = page;
            }

            return res;
        }
    }
}