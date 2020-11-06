import React from 'react';
import {InputGroup, Button, FormControl, Container, Row} from 'react-bootstrap'

const Search = () => {
    const inputstyle = {
        display: "flex",
        justifyContent: "center",
        width: "80%"
    }
    return (
        <div>
            <Container>
                <Row>
                    <InputGroup className="mb-3" style={inputstyle}>
                        <FormControl
                        aria-describedby="basic-addon2"
                        />
                        <InputGroup.Append>
                        <Button variant="outline-secondary">검색</Button>
                        </InputGroup.Append>
                    </InputGroup>
                </Row>
            </Container>
        </div>
    )
}

export default Search;