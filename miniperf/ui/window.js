import React from 'react'
import { VscTools } from 'react-icons/vsc';
import { FcOpenedFolder } from 'react-icons/fc';
import { IconContext, DiJoomla } from 'react-icons';
import { Button, ButtonGroup, Form, Table, Navbar, Nav, FormControl, NavDropdown, OverlayTrigger, Tooltip, Modal, Row, Col } from 'react-bootstrap'

class Window extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            recording: false,
            exePath: "",
            symbolPaths: "http://xsjsymbol.testplus.cn;http://127.0.0.1:80",
            outputInfo: [],
            tables: [],
            settingDialogShow: false,
            curStatus: "",
            settingPath: {} // setting弹窗渲染的配置
        }

        this.onsymbolChanged = this.onsymbolChanged.bind(this)
        this.onexeChanged = this.onexeChanged.bind(this)
        this.selectApp = this.selectApp.bind(this)
        this.onPlayClick = this.onPlayClick.bind(this)
        this.onMessage = this.onMessage.bind(this)
    }
    on_GetFileList() {
        RPC.invoke("rpc_GetFileList", {}).then(response => {
            if (response.ok) {
                console.log(response.dat)
                var list = this.filesFilter(response.dat,this.state.curStatus)
                this.setState({
                    tables: list
                })
                RPC.invoke("rpc_DefaultSetting", {dat: ""}).then(response => {
                    if (response.ok) {
                        console.log(response.dat)
                        this.setState({
                            settingPath: response.dat
                        })
                    } else {
                        alert(response.msg)
                    }
                })
            } else {
                alert(response.msg)
            }
        })
    }

    filesFilter(list,tag){
        if(tag === ''){
            return list
        }
        var tempList = []
        list.forEach(item=>{
            if(item['status'] === tag){
                tempList.push(item)
            }
        })
        return tempList
    }
    updateCurStatus(status){
        this.setState({
            curStatus: status
        },()=>{
            this.on_GetFileList()
        })
    }

    componentDidMount() {
        window.addEventListener("message", this.onMessage);
        this.on_GetFileList()
        // this.on_GetSettigPath()
    }

    componentWillUnmount() {
        window.removeEventListener("message", this.onMessage);
    }

    onChangeSettingDialog(isShow) {
        if (!isShow) {
            // this.setState({ settingPath: this.getDefaultSetting() })
        }
        this.setState({
            settingDialogShow: isShow
        })
    }

    onFolderChange(key) {
        RPC.invoke("onFolderChange", {dat: this.state.settingPath[key]}).then(response => {
            console.log("onFolderChange", response)
            if (response.ok) {

            } else {
                alert(response.msg)
            }
        })
    }

    saveSettings() {
        let obj = this.state.settingPath
        var description = "";
        for (var i in obj) {
            var property = obj[i];
            description += i + " = " + property + "\n";
        }
        alert(description);
    }

    handleInputChange(e, key) {
        const settingPath = this.state.settingPath
        settingPath[key] = e.target.value
        this.setState({
            settingPath
        })
    }

    onMessage(event) {
        let data = event.data;
        console.log("onMessage", data)
        if (data.type == "on_message") {
            data = data.data
            if (data.type == "notice" && data.msg == "stop") {
                this.setState({
                    recording: false
                })
            } else if (data.type == "out") {
                let outputInfo
                outputInfo = this.state.outputInfo
                outputInfo.push(data.msg)
                this.setState({
                    outputInfo: outputInfo
                })
            }
        }
    }


    onsymbolChanged(val) {
        this.setState({
            symbolPaths: val
        })
    }

    onexeChanged(val) {
        this.setState({
            exePath: val
        })
    }

    selectApp() {
        RPC.invoke("select_app").then(response => {
            console.log("select_app", response)
            if (response.ok) {
                this.setState({
                    exePath: response.msg,
                })
            } else {
                alert(response.msg)
            }
        })
    }

    onPlayClick() {
        if (this.state.exePath == "") {
            alert("请选择测试应用")
            return
        }
        if (this.state.recording) {
            alert("请关闭应用后,自动停止录制.")
        } else {
            this.setState({
                outputInfo: []
            })
            RPC.invoke("start", { exe_path: this.state.exePath, symbol_paths: this.state.symbolPaths }).then(response => {
                console.log("start", response)
                if (response.ok) {
                    this.setState({
                        recording: true,
                    })
                } else {
                    alert(response.msg)
                }
            })
        }
    }

    on_CheckTableClick(id, e) {
        console.log(id)
        RPC.invoke("rpc_CheckTableClick", { dat: this.state.tables[id] }).then(response => {
            if (response.ok) {
                alert(response.msg)
            } else {
                alert(response.msg)
            }
        })
    }

    on_GenCSCodeClick(id) {
        console.log(id)
        RPC.invoke("rpc_GenCSCodeClick", { dat: this.state.tables[id] }).then(response => {
            if (response.ok) {
                alert(response.dat)
            } else {
                alert(response.msg)
            }
        })
    }

    on_GenTabFileClick(id) {
        console.log(id)
        RPC.invoke("rpc_GenTabFileClick", { dat: this.state.tables[id] }).then(response => {
            if (response.ok) {
                alert(response.dat)
            } else {
                alert(response.msg)
            }
        })
    }

    on_CommitFileClick(id) {
        RPC.invoke("rpc_CommitFileClick", { dat: this.state.tables[id] }).then(response => {
            if (response.ok) {
                // alert(response.dat)
            } else {
                alert(response.msg)
            }
        })
    }

    on_OpenXlsxFileClick(id) {
        console.log(id)
        RPC.invoke("rpc_OpenXlsxFileClick", { dat: this.state.tables[id] }).then(response => {
            if (response.ok) {
                // alert(response.dat)
            } else {
                alert(response.msg)
            }
        })
    }

    on_GenCSAndTabCodeClick(id) {
        console.log(id)
        RPC.invoke("rpc_GenCSAndTabCodeClick", { dat: this.state.tables[id] }).then(response => {
            if (response.ok) {
                alert(response.dat)
            } else {
                alert(response.msg)
            }
        })

        // this.on_GenCSCodeClick(id)
        // this.on_GenTabFileClick(id)
    }

    on_CommitCSAndTabCodeClick(id) {
        console.log(id)
        RPC.invoke("rpc_CommitCSAndTabCodeClick", { dat: this.state.tables[id] }).then(response => {
            if (response.ok) {
                // alert(response.dat)
            } else {
                alert(response.msg)
            }
        })
    }

    on_CommitAllFilesClick() {
        RPC.invoke("rpc_CommitAllFilesClick", { dat: '' }).then(response => {
            if (response.ok) {
                // alert(response.dat)
            } else {
                alert(response.msg)
            }
        })
    }
    on_ConvertAllFilesClick() {
        RPC.invoke("rpc_ConvertAllFilesClick", { dat: '' }).then(response => {
            if (response.ok) {
                alert(response.dat)
            } else {
                alert(response.msg)
            }
        })
    }
    render() {

        const renderTooltip = (props) => (
            <Tooltip id="button-tooltip" {...props}>
                Simple tooltip
            </Tooltip>
        );


        const outContent = this.state.outputInfo.map(item => {
            return <p style={{ textIndent: "2em" }}>{item}</p>
        })

        return (
            <div>
                <Navbar bg="primary" variant="dark">
                    <Navbar.Brand href="#home">
                        <IconContext.Provider value={{ size: "2em" }}>
                            <VscTools />
                        </IconContext.Provider>

                    </Navbar.Brand>
                    <Nav className="mr-auto nav nav-tabs">
                        <Nav.Link onClick={() => this.updateCurStatus('')} autoFocus={true} data-toggle="tab">All</Nav.Link>
                        <Nav.Link onClick={() => this.updateCurStatus('M')} autoFocus={true} data-toggle="tab">Changed</Nav.Link>
                        <Nav.Link onClick={() => this.updateCurStatus('?')} autoFocus={true} data-toggle="tab">New</Nav.Link>
                        <Nav.Link onClick={() => this.onChangeSettingDialog(true)}>Setting</Nav.Link>
                    </Nav>
                    <Form inline>
                        <FormControl type="text" placeholder="Search" className="mr-sm-2" />
                        {/* <Button variant="outline-light">Search</Button> */}
                    </Form>
                    <Button variant="primary" onClick={() => this.on_GetFileList()} >刷新</Button>
                    <Button variant="primary" onClick={() => this.on_ConvertAllFilesClick()} >一键转换所有表格</Button>
                    <Button variant="primary" onClick={() => this.on_CommitAllFilesClick()} >提交所有修改记录</Button>
                </Navbar>

                <br />
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>表格名称</th>
                            <th>策划使用</th>
                            <th>程序使用</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.tables.map((value, index) => {
                            return (
                                <tr key={index}>
                                    <td>{index}</td>
                                    <td>{value.name}</td>
                                    <td>
                                        <ButtonGroup aria-label="Basic example">
                                            <Button variant="primary" onClick={() => this.on_OpenXlsxFileClick(index)} >打开</Button>
                                            <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }} overlay={renderTooltip} >
                                                <Button variant="success" id={index} onClick={() => this.on_CheckTableClick(index)} >检正确性</Button>
                                            </OverlayTrigger>
                                            <Button variant="primary" onClick={() => this.on_GenTabFileClick(index)} >生成.csv</Button>
                                            <Button variant="primary" onClick={() => this.on_CommitFileClick(index)} >提交</Button>
                                        </ButtonGroup>
                                    </td>
                                    <td>
                                        <ButtonGroup aria-label="Basic example">
                                            <Button variant="primary" onClick={() => this.on_GenCSAndTabCodeClick(index)} >生成.CS/.csv</Button>
                                            <Button variant="primary" onClick={() => this.on_CommitCSAndTabCodeClick(index)} >提交</Button>
                                        </ButtonGroup>
                                    </td>
                                </tr>
                            )
                        })}
                    </tbody>
                </Table>

                <Modal show={this.state.settingDialogShow} centered={true} size='lg' onHide={() => this.onChangeSettingDialog(false)} >
                    <Modal.Header closeButton>
                        <Modal.Title id="example-custom-modal-styling-title">
                            Settings
                    </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            {
                                Object.keys(this.state.settingPath).map((item, index) => (
                                    <Form.Group as={Row} controlId="formHorizontalEmail" key={`${item}_${index}`}>
                                        <Form.Label column sm={2}>
                                            {item}
                                        </Form.Label>
                                        <Col sm={9}>
                                            <Form.Control placeholder={item} value={this.state.settingPath[item]} onChange={(e) => this.handleInputChange(e, item)} />
                                        </Col>
                                        <Col sm={1}>
                                            <IconContext.Provider value={{ size: "25px", style: { cursor: 'pointer' } }}>
                                                <FcOpenedFolder onClick={() => this.onFolderChange(item)} />
                                            </IconContext.Provider>
                                        </Col>
                                    </Form.Group>
                                ))
                            }
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={() => this.onChangeSettingDialog(false)}> Close </Button>
                        <Button variant="primary" onClick={() => this.saveSettings()} >Save changes</Button>
                    </Modal.Footer>
                </Modal>
            </div>
        )
    }
}

export default Window