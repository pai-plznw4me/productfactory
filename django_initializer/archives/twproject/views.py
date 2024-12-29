from django.shortcuts import render
from file.models import File


def index(request):
    ret = '''{"tasks": [
        {"id": -1, "name": "Gantt editor", "progress": 0, "progressByWorklog": false, "relevance": 0, "type": "",
         "typeId": "", "description": "", "code": "", "level": 0, "status": "STATUS_ACTIVE", "depends": "",
         "canWrite": true, "start": 1396994400000, "duration": 20, "end": 1399586399999, "startIsMilestone": false,
         "endIsMilestone": false, "collapsed": false, "assigs": [], "hasChild": true},
        {"id": -2, "name": "coding", "progress": 0, "progressByWorklog": false, "relevance": 0, "type": "",
         "typeId": "", "description": "", "code": "", "level": 1, "status": "STATUS_ACTIVE", "depends": "",
         "canWrite": true, "start": 1396994400000, "duration": 10, "end": 1398203999999, "startIsMilestone": false,
         "endIsMilestone": false, "collapsed": false, "assigs": [], "hasChild": true},
        {"id": -3, "name": "gantt part", "progress": 0, "progressByWorklog": false, "relevance": 0, "type": "",
         "typeId": "", "description": "", "code": "", "level": 2, "status": "STATUS_ACTIVE", "depends": "",
         "canWrite": true, "start": 1396994400000, "duration": 2, "end": 1397167199999, "startIsMilestone": false,
         "endIsMilestone": false, "collapsed": false, "assigs": [], "hasChild": false},
        {"id": -4, "name": "editor part", "progress": 0, "progressByWorklog": false, "relevance": 0, "type": "",
         "typeId": "", "description": "", "code": "", "level": 2, "status": "STATUS_SUSPENDED", "depends": "3",
         "canWrite": true, "start": 1397167200000, "duration": 4, "end": 1397685599999, "startIsMilestone": false,
         "endIsMilestone": false, "collapsed": false, "assigs": [], "hasChild": false},
        {"id": -5, "name": "testing", "progress": 0, "progressByWorklog": false, "relevance": 0, "type": "",
         "typeId": "", "description": "", "code": "", "level": 1, "status": "STATUS_SUSPENDED", "depends": "2:5",
         "canWrite": true, "start": 1398981600000, "duration": 5, "end": 1399586399999, "startIsMilestone": false,
         "endIsMilestone": false, "collapsed": false, "assigs": [], "hasChild": true},
        {"id": -6, "name": "test on safari", "progress": 0, "progressByWorklog": false, "relevance": 0, "type": "",
         "typeId": "", "description": "", "code": "", "level": 2, "status": "STATUS_SUSPENDED", "depends": "",
         "canWrite": true, "start": 1398981600000, "duration": 2, "end": 1399327199999, "startIsMilestone": false,
         "endIsMilestone": false, "collapsed": false, "assigs": [], "hasChild": false},
        {"id": -7, "name": "test on ie", "progress": 0, "progressByWorklog": false, "relevance": 0, "type": "",
         "typeId": "", "description": "", "code": "", "level": 2, "status": "STATUS_SUSPENDED", "depends": "6",
         "canWrite": true, "start": 1399327200000, "duration": 3, "end": 1399586399999, "startIsMilestone": false,
         "endIsMilestone": false, "collapsed": false, "assigs": [], "hasChild": false},
        {"id": -8, "name": "test on chrome", "progress": 0, "progressByWorklog": false, "relevance": 0, "type": "",
         "typeId": "", "description": "", "code": "", "level": 2, "status": "STATUS_SUSPENDED", "depends": "6",
         "canWrite": true, "start": 1399327200000, "duration": 2, "end": 1399499999999, "startIsMilestone": false,
         "endIsMilestone": false, "collapsed": false, "assigs": [], "hasChild": false},
    ], "selectedRow": 2, "deletedTaskIds": [],
        "resources": [
            {"id": "tmp_1", "name": "Resource 1"},
            {"id": "tmp_2", "name": "Resource 2"},
            {"id": "tmp_3", "name": "Resource 3"},
            {"id": "tmp_4", "name": "Resource 4"}
        ],
        "roles": [
            {"id": "tmp_1", "name": "Project Manager"},
            {"id": "tmp_2", "name": "Worker"},
            {"id": "tmp_3", "name": "Stakeholder"},
            {"id": "tmp_4", "name": "Customer"}
        ], "canWrite": true, "canDelete": true, "canWriteOnParent": true, "canAdd": true}'''

    ret2 = '''
    {
        "tasks": [
            {
                "id": "tmp_fk1345624806538",
                "name": "Gantt editor ",
                "code": "123",
                "level": 0,
                "status": "STATUS_ACTIVE",
                "start": 1346623200000,
                "duration": 5,
                "end": 1347055199999,
                "startIsMilestone": false,
                "endIsMilestone": false,
                "assigs": [
                    {
                        "resourceId": "tmp_3",
                        "id": "tmp_1345625008213",
                        "roleId": "tmp_1",
                        "effort": 7200000
                    },
                    {
                        "resourceId": "tmp_3",
                        "id": "tmp_1345625008213",
                        "roleId": "tmp_1",
                        "effort": 7200000
                    }

                    
                ],
                "depends": "",
                "description": "",
                "progress": 0
            },
            {
                "id": "tmp_fk1345624806539",
                "name": "phase 1",
                "code": "",
                "level": 1,
                "status": "STATUS_ACTIVE",
                "start": 1346623200000,
                "duration": 2,
                "end": 1346795999999,
                "startIsMilestone": false,
                "endIsMilestone": false,
                "assigs": [
                    {
                        "resourceId": "tmp_1",
                        "id": "tmp_1345624980735",
                        "roleId": "tmp_1",
                        "effort": 36000000
                    }
                ],
                "depends": "",
                "description": "",
                "progress": 0
            },
            {
                "id": "tmp_fk1345624789530",
                "name": "phase 2",
                "code": "",
                "level": 1,
                "status": "STATUS_SUSPENDED",
                "start": 1346796000000,
                "duration": 3,
                "end": 1347055199999,
                "startIsMilestone": false,
                "endIsMilestone": false,
                "assigs": [
                    {
                        "resourceId": "tmp_2",
                        "id": "tmp_1345624993405",
                        "roleId": "tmp_2",
                        "effort": 36000000
                    }
                ],
                "depends": "2",
                "description": "",
                "progress": 0
            }
        ],
        "resources": [
            {
                "id": "tmp_1",
                "name": "Resource 1"
            },
            {
                "id": "tmp_2",
                "name": "Resource 2"
            },
            {
                "id": "tmp_3",
                "name": "Resource 3"
            }
        ], "roles": [
        {
            "id": "tmp_1",
            "name": "Project Manager"
        },
        {
            "id": "tmp_2",
            "name": "Worker"
        }
    ],
        "canWrite": true,
        "canWriteOnParent": true,
        "canAdd":true,
        "selectedRow": 0,
        "deletedTaskIds": [],
    }
    '''

    context = {'infos': ret2, 'title': '불법판독시스템'}
    return render(request, template_name='twproject/gantt.html', context=context)

def load(request, fileid):
    file = File.objects.get(id=fileid)
    filepath = file.filecontent.path
    ret = open(filepath, 'r').read()
    context = {'infos': ret, 'title': '불법판독시스템'}
    return render(request, template_name='twproject/gantt.html', context=context)
