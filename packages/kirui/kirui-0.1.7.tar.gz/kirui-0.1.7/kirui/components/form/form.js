import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h } from 'preact';
import $ from "jquery";


class Form extends Component {
    constructor(props) {
        super(props);

        this.state = {
            'csrfmiddlewaretoken': this.props.csrfmiddlewaretoken
        }

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.bubbleStateChange = this.bubbleStateChange.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;

        let name, value;
        if (event.detail !== undefined) {
            name = event.target.getAttribute('name');
            value = event.detail.data;
        } else {
            name = target.name;
            value = target.type === 'checkbox' ? target.checked : target.value;
        }

        this.setState({[name]: value});
        $.extend(this.state, {[name]: value});
    }

    bubbleStateChange(orig_event) {
        let params = {bubbles: true, detail: {'data': this.state}}
        if (orig_event !== undefined) {
            orig_event.preventDefault();
            orig_event.stopPropagation();
            params.detail.forceUpdate = true;
        } else {
            params.detail.forceUpdate = false;
        }

        let event = new CustomEvent('StateChange', params);
        this.base.dispatchEvent(event);
    }

    handleSubmit(event) {
        event.preventDefault();
        if (event.submitter.name) {
            this.state[event.submitter.name] = ''
        }

        let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': true}});
        this.base.dispatchEvent(e);

        $.post({
            url: this.props.action || window.location,
            data: $.param(this.state, true),
            statusCode: {
                340: function (resp) {
                    window.location.replace(resp.getResponseHeader('location'));
                    console.log(resp.getResponseHeader('location'));
                }
            }
        }).done((resp, status, xhr) => {
            console.log(resp, status, xhr)

            let dom = resp;
            this.dataToCreateElement([dom]);
            this.props.children = dom[2];
            this.forceUpdate();

            let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
            this.base.dispatchEvent(e);
        }).fail((resp) => {
            if (resp.status === 403) {
                let dom = resp.responseJSON;
                this.dataToCreateElement([dom]);
                this.props.children = dom[2];
                this.forceUpdate();

                let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
                this.base.dispatchEvent(e);
            } else if (resp.status === 302) {
                console.log(resp)
            }
        });
    }

    doRender() {
        return <form {...this.props} onHandleInputChange={this.handleInputChange}>
            {this.props.children}
        </form>
    }

    componentDidMount() {
        if (this.props.didMountCallback) {
            this.bubbleStateChange();
        }
    }
}

registry.register('kr-form', Form);
export { Form }