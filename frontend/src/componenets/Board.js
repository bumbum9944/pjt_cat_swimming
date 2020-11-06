import React from 'react'
import {Table, Button, Modal, Form} from 'react-bootstrap'
import axios from 'axios'

const Board = ({realdata, filterState}) => {
    const [show, setShow] = React.useState(false);
    const handleClose = () => setShow(false);
    const [reportdata, setReportdata] = React.useState({});
    const [optionState, setOptionState] = React.useState("1");
    const handleSelect = (e) => {
        setOptionState(e.target.value)
    }
    const handleShow = (data) => {
        setShow(true)
        setReportdata(data)
    }
    const report = (data) => {
        console.log(optionState)
        data.report = optionState
        console.log(data)
        axios.post("http://i02c102.p.ssafy.io:5000/report", data)
        .then((res)=>{
            console.log(res)
        })
        .catch((e)=>{
            console.log(e)
        })
        handleClose()
    }

    const adButton = (data) => {
        const num = data.isTrader
        if (num > 0.5){
            return <Button onClick={()=>handleShow(data)} style={{fontSize:"12px"}} size="sm" variant="danger">위험</Button>
        }
        else if (num > 0.3){
            return <Button onClick={()=>handleShow(data)} style={{fontSize:"12px"}} size="sm" variant="warning">의심</Button>
        }
        return <Button onClick={()=>handleShow(data)} style={{fontSize:"12px"}} size="sm" variant="primary">일반</Button>
    }

    const eachdata = (data, index, advalue) => {
        if (filterState === "2"){
            if (advalue > 0.3){
                return <></>
            }
        }
        else if (filterState === "3"){
            if (advalue > 0.5){
                return <></>
            }
        }
        return  (
            <tr key={index}>
                <td className="text-center" style={{fontSize: "12px"}}>{data.category}</td>
                <td><a href={data.url} target="_blank" style={{color: "black"}}>{data.title}</a></td>    
                <td className="text-center" style={{fontSize: "10px"}}>{data.user}</td>
                <td className="text-center" style={{fontSize: "12px"}}>{data.date}</td>
                <td className="text-center">{adButton(data)}</td>
            </tr>
        )

    }
    return (
        <>
            <Table responsive>
                <thead>
                <tr>
                    <th className="text-center" style={{width: "10%"}}>카테고리</th>
                    <th className="text-center" style={{width: "66%"}}>제목</th>
                    <th className="text-center" style={{width: "8%"}}>작성자</th>
                    <th className="text-center" style={{width: "8%"}}>작성일</th>
                    <th className="text-center" style={{width: "8%"}}>광고</th>
                </tr>
                </thead>
                <tbody>
                    {realdata.map((data, index) => eachdata(data, index, data.isTrader))}
                </tbody>

                <Modal show={show} onHide={handleClose} centered>
                    <Modal.Header closeButton>
                    <Modal.Title>신고하기</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group controlId="exampleForm.SelectCustom">
                                <Form.Label>사유선택: </Form.Label>
                                <Form.Control as="select" custom value={optionState} onChange={handleSelect}>
                                    <option value="1">광고글이 일반으로 표시됨</option>
                                    <option value="2">일반글이 광고글로 표시됨</option>
                                    <option value="3">기타 확인필요</option>
                                </Form.Control>
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        닫기
                    </Button>
                    <Button variant="primary" onClick={()=>report(reportdata)}>
                        신고하기
                    </Button>
                    </Modal.Footer>
                </Modal>
            </Table>
        </>
    )
}

export default Board