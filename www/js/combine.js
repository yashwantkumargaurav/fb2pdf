var id = 0;

function addURL()
{
    addElement(false);
}

function addFile()
{
    addElement(true);
}

function addElement(file)
{
    var tab = document.getElementById('filetable');
    var n = tab.rows.length;
  
    var row=tab.insertRow(n);
    row.id = "row"+id; 
    var c0=row.insertCell(0);
    var c1=row.insertCell(1);
    if(file)
        c0.innerHTML="<input type=\"file\" name=\"fileupload"+id+"\" size=\"25\"/>";
    else
        c0.innerHTML="<input type=\"text\" id=\"fileupload\" value=\"наберите URL здесь\" name=\"url"+id+"\" size=\"30\"/>";
    c1.innerHTML="<input type=\"button\" onclick=\"removeRow("+id+");\" value=\"-\"/>";
    id++;
    showTable(true);
}

function removeRow(rid)
{
    var tab = document.getElementById('filetable');
    var nr=tab.rows.length;
    for(i=0;i<nr;i++)
        if(tab.rows[i].id=="row"+rid)
        {
            tab.deleteRow(i);
            if(nr==1)
                showTable(false);
            break;
        }
}

function showTable(x)
{
    if(x)
    {
        document.getElementById('filetable').style.display='block';
        document.getElementById('nobooks').style.display='none';
    } else
    {
        document.getElementById('filetable').style.display='none';
        document.getElementById('nobooks').style.display='block';
    }

}
